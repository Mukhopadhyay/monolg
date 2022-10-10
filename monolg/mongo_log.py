"""Main script containing the classes"""

# Built-in modules
import os
import warnings
from configparser import RawConfigParser
from typing import Optional, Dict, Any

# Third-party
import pymongo

# Custom modules
from monolg import utils
from monolg import _schemas
from monolg.errors import ConnectionNotEstablishedErr, InvalidLevelWarning, NotConnectedWarning, ConnectionNotReopened

# Setting up the global configs
config = RawConfigParser()
config.read(os.path.join("monolg", "configs.ini"))


POSSIBLE_LEVELS = ("info", "warning", "error", "critical")


class Monolg(object):
    """Main class for Monolg.

    Args:
        object (_type_): _description_

    Raises:
        ConnectionNotEstablishedErr: Gets raised when connection could not be established with Mongo.
        ConnectionNotReopened: This exception gets raised if the object is instantiated using some classmethod and
                               then an attempt to reconnect to the mongo db is made (using self.reopen())

    Levels:
        info:       Default logging level
        warning:    Warnings should be called when something unexpected happens but it isn't code-breaking. (but probably needs attention)
        error:      Some exception that caused the system to malfunction.
        critical:   Some serious error has occured, that requires your attention.

    """

    # Default settings
    # If None if found on the kwargs of the constructor
    # These values will be used instead.
    HOST: str = config["MONGO"]["HOST"]
    PORT: int = int(config["MONGO"]["PORT"])
    TIMEOUT: int = int(config["MONGO"]["TIMEOUT"])

    # Default logger settings
    NAME: str = config["DEFAULT"]["PROJECT_NAME"].capitalize()
    LEVEL: str = config["SETTINGS"]["LEVEL"]
    DT_FMT: str = config["SETTINGS"]["DT_FMT"]

    DEFAULT_DB_NAME: str = config["DEFAULT"]["PROJECT_NAME"].capitalize()
    DEFFAULT_COLLECTION_NAME: str = config["MONGO"]["DEFAULT_COLLECTION_NAME"]

    SCHEMA = {
        "info": _schemas.Info,
        "warning": _schemas.Warning,
        "error": _schemas.Error,
        "critical": _schemas.Critical,
    }

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        name: Optional[str] = None,
        level: Optional[str] = None,
        serv_sel_timeout: Optional[int] = None,
        client: Optional[pymongo.MongoClient] = None,
        verbose: Optional[bool] = False,
        # If set to True, then it'll create a seperate collection & log, this package's info
        system_log: Optional[bool] = True,
        **kwargs,
    ) -> None:

        # If nothing passed 'localhost' will be used
        self.host: Optional[str] = host
        if not self.host:
            self.host = self.HOST

        # If nothing passed, 27017 will be used
        self.port: Optional[int] = port
        if not self.port:
            self.port = self.PORT

        # Default name to use for logs, if nothing passed 'Monolg' will be used
        self.name: Optional[str] = name
        if not self.name:
            self.name = self.NAME

        # Defaults to info
        self.level: Optional[str] = level
        if not self.level:
            self.level = self.LEVEL

        self.serv_sel_timeout: Optional[int] = serv_sel_timeout
        if not serv_sel_timeout:
            self.serv_sel_timeout = self.TIMEOUT

        self.filename: Optional[str] = None
        try:
            self.filename = __file__
        except NameError:
            # In notebooks __file__ won't work
            pass

        # Following will be populated after .connect() is invoked
        self.db: pymongo.database.Database = None
        self.collection: pymongo.collection.Collection = None
        self._sys_collection: pymongo.collection.Collection = None

        # These will be populated later
        self.db_name = None
        self.collection_name = None

        #########
        # Flags #
        #########

        self.verbose = verbose
        self.sys_log = system_log
        # Is this instance connected to Mongo??
        self.__connected = False
        # Is the system log collection connected to Mongo??
        self.__sys_connected = False
        # Is this object instantiated using the client?
        self.__is_from_client = kwargs.get("is_from_client", False)

        self.client: pymongo.MongoClient = client
        if not self.client:
            self.client = pymongo.MongoClient(
                host=self.host, port=self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
            )

    @classmethod
    def from_connection(cls, client: pymongo.MongoClient) -> object:
        # TODO: If this is how its instantiated
        # then the connection cannot be reopened
        return cls(client=client, is_from_client=True)

    def __test_connection(self) -> None:
        try:
            # Test out a connection
            __test_client: pymongo.MongoClient = pymongo.MongoClient(
                self.host, self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
            )
            __test_client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            raise ConnectionNotEstablishedErr()

    def connect(self, db: Optional[str] = None, collection: Optional[str] = None) -> None:
        self.db_name = db
        self.collection_name = collection

        if not self.db_name:
            self.db_name = self.DEFAULT_DB_NAME

        if not self.collection_name:
            self.collection_name = self.DEFFAULT_COLLECTION_NAME

        self.__test_connection()

        self.db = self.client.get_database(self.db_name)
        self.collection: pymongo.collection.Collection = self.db.get_collection(self.collection_name)
        if self.sys_log:
            self._sys_collection = self.db.get_collection("__monolg")
            self.__sys_connected = True

        self.__connected = True
        if self.__sys_connected:
            # Log that monolg is connection
            self.log("monolg connected to mongodb", "system", "info", collection=self._sys_collection)

    def reopen(self) -> None:
        """Reopens the network, reinitializes the MongoClient"""

        # If this object was creating using a client then raise
        if self.__is_from_client:
            raise ConnectionNotReopened(
                "Cannot re-establish connection. Object was instantiated using client.\nTry instantiating using the constructor."
            )

        self.client = pymongo.MongoClient(
            host=self.host, port=self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
        )
        self.connect(self.db_name, self.collection_name)
        if self.sys_log:
            if self.__sys_connected:
                # Log that monolg is connection
                self.log("monolg connection reopened", "system", "info", collection=self._sys_collection)

    def close(self) -> None:
        """Closes connection
        Read more here:
        https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient.close

        A connection pool still keeps running, so if we perform some op this
        connection will be re-opened.
        https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        """
        if self.__connected:
            if self.sys_log:
                if self.__sys_connected:
                    # Log that monolg is connection
                    self.log("monolg connection with mongodb closed", "system", "info", collection=self._sys_collection)

            self.client.close()
            self.__connected = False

    def __insert_model(self, level: str, collection: Optional[pymongo.collection.Collection] = None, **kwargs) -> None:
        # Model to use
        model = self.SCHEMA.get(level)

        if not model:
            msg = f"Invalid level '{level}' logging on info instead. Use one of {POSSIBLE_LEVELS}"
            warnings.warn(msg, category=InvalidLevelWarning)
            model = self.SCHEMA.get("info")

        # Instantiate the schema model based on the keyword arguments
        log_model = model(**kwargs)

        # If collection is passed in param, we'll be using that
        # else we'll end up using the default monolg collection
        if isinstance(collection, pymongo.collection.Collection):
            collection = collection
        else:
            collection = self.collection

        collection.insert_one(log_model.to_dict())

    def log(
        self,
        message: str,
        name: Optional[str] = None,
        level: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        datetime_as_string: Optional[bool] = False,  # Defaults to setting it as datetime objects
        datetime_fmt: Optional[str] = None,
        verbose: Optional[bool] = True,  # This overrides the instance attribute for verbose
        **kwargs,
    ) -> None:
        if not self.__connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)
        if not level:
            level: str = self.level

        fmt: str = datetime_fmt
        if not fmt:
            fmt = self.DT_FMT

        dt = utils.get_datetime(datetime_as_string, fmt)

        name = name if name else self.name
        self.__insert_model(level, name=name, message=message, time=dt, data=data, file=self.filename, **kwargs)
        if self.verbose and verbose:
            utils.print_log(dt, message, level.upper(), name, fmt=self.DT_FMT)

    def info(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        self.log(message, name, "info", data, **kwargs)

    def warning(
        self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> None:
        self.log(message, name, "warning", data, **kwargs)

    def error(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        self.log(message, name, "error", data, **kwargs)

    def critical(
        self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> None:
        self.log(message, name, "critical", data, **kwargs)

    def clear_logs(self) -> None:
        if not self.__connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)
        self.collection.delete_many({})

        if self.sys_log:
            if self.__sys_connected:
                self.log("All monolg logs cleared", "system", "warning", collection=self._sys_collection)
