"""
Main script containing the classes
"""

# Built-in modules
import os
import warnings
from datetime import datetime
from typing import Optional, Dict, Any
from configparser import RawConfigParser

# Third-party
import pymongo

# Custom modules
from monolg import utils
from monolg import _schemas
from monolg.errors import (
    ConnectionNotEstablishedErr,
    InvalidLevelWarning,
    NotConnectedError,
    NotConnectedWarning,
    ConnectionNotReopened,
)

# Setting up the global configs
config = RawConfigParser()
config.read(os.path.join("monolg", "configs.ini"))

POSSIBLE_LEVELS = ("info", "warning", "error", "critical")


class Monolg(object):
    """Main class for Monolg.

    Raises:
        ConnectionNotEstablishedErr: Gets raised when connection could not be established with Mongo.
        ConnectionNotReopened: This exception gets raised if the object is instantiated using some classmethod and
        then an attempt to reconnect to the mongo db is made (using self.reopen())

    Levels:
        info:       Default logging level
        warning:    Warnings should be called when something unexpected happens
                    but it isn't code-breaking. (but probably needs attention)
        error:      Some exception that caused the system to malfunction.
        critical:   Some serious error has occured that requires your attention.

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

    SCHEMA: Dict[str, Any] = {
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
        verbose: Optional[bool] = True,
        sys_verbose: Optional[bool] = True,
        # If set to True, then it'll create a seperate collection & log, this package's info
        system_log: Optional[bool] = True,
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            host (Optional[str], optional): _description_. Defaults to None.
            port (Optional[int], optional): _description_. Defaults to None.
            name (Optional[str], optional): _description_. Defaults to None.
            level (Optional[str], optional): _description_. Defaults to None.
            serv_sel_timeout (Optional[int], optional): _description_. Defaults to None.
            client (Optional[pymongo.MongoClient], optional): _description_. Defaults to None.
            verbose (Optional[bool], optional): _description_. Defaults to True.
            sys_verbose (Optional[bool], optional): _description_. Defaults to True.
            system_log (Optional[bool], optional): _description_. Defaults to True.
        """

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
            pass  # In notebooks __file__ won't work

        # Following will be populated after .connect() is invoked
        self.db: Optional[pymongo.database.Database] = None
        self.collection: Optional[pymongo.collection.Collection] = None
        self._sys_collection: Optional[pymongo.collection.Collection] = None

        self.__connection_time: Optional[datetime] = None

        # These will be populated later
        self.db_name = None
        self.collection_name = None

        #########
        # Flags #
        #########

        self.verbose = verbose
        self.sys_verbose = sys_verbose

        # Should we be logging monolg's system logs?
        self.sys_log: bool = system_log
        # Is this instance connected to Mongo?
        self.__connected: bool = False
        # Was this instance previously connected?
        self.__connected_before: bool = False
        # Is the system log collection connected to Mongo??
        self.__sys_connected: bool = False
        # Is this object instantiated using the client?
        self.__is_from_client: bool = kwargs.get("is_from_client", False)

        self.client: Optional[pymongo.MongoClient] = client
        if not self.client:
            self.client = pymongo.MongoClient(
                host=self.host, port=self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
            )

    @classmethod
    def from_client(cls, client: pymongo.MongoClient, **kwargs) -> object:
        """Allows instantiation from an existing pymongo.MongoClient object.
        Please note that in this case, if the connection is ever closed, we will not be
        able to "reopen" the connection using Monolg.reopen()

        Please refer to this page on further docs:
        https://monolg.readthedocs.io/en/latest/connecting-monolg/#instantiating-from-an-existing-connection

        Args:
            client (pymongo.MongoClient): _description_

        Returns:
            object: _description_
        """
        return cls(client=client, is_from_client=True, **kwargs)

    @property
    def connection_time(self) -> datetime:
        """Returns when the instance was connected to MongoDB"""
        return self.__connection_time

    @property
    def connected(self) -> bool:
        """Returns the connected flag, True means the instance is connected to MongoDB"""
        return self.__connected

    @property
    def sys_connected(self) -> bool:
        """Returns true if the system logs database is created / connected"""
        return self.__sys_connected

    @property
    def is_from_client(self) -> bool:
        """Returns true if this instance was creating using the classmethod Monolg.from_client(client)"""
        return self.__is_from_client

    @property
    def connected_before(self) -> bool:
        """Returns true if this instance was connected to mongo before"""
        return self.__connected_before

    def __test_connection(self) -> None:
        """_summary_

        Raises:
            ConnectionNotEstablishedErr: _description_
        """
        try:
            # Test out a connection
            __test_client: pymongo.MongoClient = pymongo.MongoClient(
                self.host, self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
            )
            __test_client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            raise ConnectionNotEstablishedErr()

    def connect(self, db: Optional[str] = None, collection: Optional[str] = None) -> None:
        """_summary_

        Args:
            db (Optional[str], optional): _description_. Defaults to None.
            collection (Optional[str], optional): _description_. Defaults to None.
        """
        self.db_name = db
        self.collection_name = collection

        if not self.db_name:
            self.db_name = self.DEFAULT_DB_NAME

        if not self.collection_name:
            self.collection_name = self.DEFFAULT_COLLECTION_NAME

        # Test connection
        self.__test_connection()

        self.db = self.client.get_database(self.db_name)

        # Save the connection time
        self.__connection_time = utils.get_datetime()

        # Create the system collection first
        if self.sys_log:
            self._sys_collection = self.db.get_collection("__monolg")
            self.__sys_connected = True

        if self.__sys_connected:
            data = {"database": self.db_name, "collection": self.collection_name, "time": self.__connection_time}
            self.log(
                f"monolg connected to mongodb",
                "system",
                "info",
                collection=self._sys_collection,
                data=data,
                verbose=self.sys_verbose,
            )

        # Create the log collection
        self.collection: pymongo.collection.Collection = self.db.get_collection(self.collection_name)
        self.__connected = True
        self.__connected_before = True

    def reopen(self) -> None:
        """_summary_

        Raises:
            ConnectionNotReopened: _description_
        """
        # If this object was creating using a client then raise
        message = """Cannot re-establish connection. Object was instantiated using client.
        Try instantiating using the constructor."""
        if self.__is_from_client:
            raise ConnectionNotReopened(message)

        message = "This instance was not connected previous, try doing object.connect() first."
        if not self.__connected_before:
            raise ConnectionNotReopened(message)

        self.client = pymongo.MongoClient(
            host=self.host, port=self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
        )
        self.connect(self.db_name, self.collection_name)
        if self.sys_log:
            if self.__sys_connected:
                # Log that monolg is connected
                data = {"database": self.db_name, "collection": self.collection_name, "time": self.__connection_time}
                self.log(
                    "monolg connection reopened",
                    "system",
                    "info",
                    collection=self._sys_collection,
                    data=data,
                    verbose=self.sys_verbose,
                )

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
                    data = {"database": self.db_name, "collection": self.collection_name, "time": self.__connection_time}
                    # Log that monolg connection to Mongo is closed
                    self.log(
                        "monolg connection with mongodb closed",
                        "system",
                        "info",
                        collection=self._sys_collection,
                        data=data,
                        verbose=self.sys_verbose,
                    )

            self.client.close()
            self.__connected = False

    def __insert_model(self, level: str, collection: Optional[pymongo.collection.Collection] = None, **kwargs) -> None:
        """_summary_

        Args:
            level (str): _description_
            collection (Optional[pymongo.collection.Collection], optional): _description_. Defaults to None.
        """

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
        datetime_as_string: bool = False,  # Defaults to setting it as datetime objects
        datetime_fmt: Optional[str] = None,
        verbose: Optional[bool] = True,  # This overrides the instance attribute for verbose
        **kwargs,
    ) -> None:
        """Logs the message and accompanying fields in MongoDB. Most of the arguments
        to this method are optional if nothing is provided, then the default or the values
        provided while instantiating `Monolg` will be used.


        Args:
            message (str): The message that is to be logged.
            name (Optional[str], optional): Name of this particular log operation, if nothing provided
                                            value from self.name will be taken, else `Monolg` will be used.
            level (Optional[str], optional): The level of logging, possible values can be 'info', 'warning',
                                             'critical' & 'error'. If nothign is provided then the level provided
                                             while creating the object will be used. If nothing was provided
                                             level will default to 'info'.
                                             Defaults to None.
            data (Optional[Dict[str, Any]], optional): Accepts any dictionary which is to be saved as
                                                       'data' in the corresponding mongo db entry.
                                                       Defaults to None.
            datetime_as_string (Optional[bool], optional): Whether to save the datetime as string or datetime object.
                                                           Defaults to False.
            verbose (Optional[bool], optional): If this flag is set then the message will be displayed in
                                                the standard output as well.
                                                Defaults to True.
        """
        # Check for both regular collection & system collection flag
        if (not self.__connected) and (not self.__sys_connected):
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            raise NotConnectedError(msg)

        if not level:
            level = self.level

        fmt: str = datetime_fmt
        if not fmt:
            fmt = self.DT_FMT

        dt = utils.get_datetime(datetime_as_string, fmt)

        name = name if name else self.name
        self.__insert_model(level, name=name, message=message, time=dt, data=data, file=self.filename, **kwargs)
        if self.verbose and verbose:
            utils.print_log(dt, message, level.upper(), name, fmt=self.DT_FMT)

    def info(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Logs a message with level INFO on this logger.

        Args:
            message (str): The message that is to be logged.
            name (Optional[str], optional): Name of this particular log operation, if nothing provided
                                            value from self.name will be taken, else `Monolg` will be used.
                                            Defaults to None.
            data (Optional[Dict[str, Any]], optional): Accepts any dictionary which is to be saved as
                                                       'data' in the corresponding mongo db entry.
                                                       Defaults to None.
        """
        self.log(message, name, "info", data, **kwargs)

    def warning(
        self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> None:
        """Logs a message with level WARNING on this logger

        Args:
            message (str): The message that is to be logged.
            name (Optional[str], optional): Name of this particular log operation, if nothing provided
                                            value from self.name will be taken, else `Monolg` will be used.
                                            Defaults to None.
            data (Optional[Dict[str, Any]], optional): Accepts any dictionary which is to be saved as
                                                       'data' in the corresponding mongo db entry.
                                                       Defaults to None.
        """
        self.log(message, name, "warning", data, **kwargs)

    def error(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """Logs a message with level ERROR on this logger

        Args:
            message (str): The message that is to be logged.
            name (Optional[str], optional): Name of this particular log operation, if nothing provided
                                            value from self.name will be taken, else `Monolg` will be used.
                                            Defaults to None.
            data (Optional[Dict[str, Any]], optional): Accepts any dictionary which is to be saved as
                                                       'data' in the corresponding mongo db entry.
                                                       Defaults to None.
        """
        self.log(message, name, "error", data, **kwargs)

    def critical(
        self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> None:
        """Logs a message with level CRITICAL on this logger

        Args:
            message (str): The message that is to be logged.
            name (Optional[str], optional): Name of this particular log operation, if nothing provided
                                            value from self.name will be taken, else `Monolg` will be used.
                                            Defaults to None.
            data (Optional[Dict[str, Any]], optional): Accepts any dictionary which is to be saved as
                                                       'data' in the corresponding mongo db entry.
                                                       Defaults to None.
        """
        self.log(message, name, "critical", data, **kwargs)

    # TODO: Should we keep this??
    def clear_logs(self) -> None:
        """Clears all logs from the currently set monolg collection. Be careful about using this"""
        if not self.__connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)

        else:
            self.collection.delete_many({})

            if self.sys_log:
                if self.__sys_connected:
                    data = {"database": self.db_name, "collection": self.collection_name, "time": self.__connection_time}
                    self.log(
                        "All monolg logs cleared",
                        "system",
                        "warning",
                        collection=self._sys_collection,
                        data=data,
                        verbose=self.sys_verbose,
                    )

    # TODO: Same... Should we keep this?
    def clear_sys_logs(self) -> None:
        """Clears all monolg system generated logs"""
        if not self.__sys_connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)
        else:
            self._sys_collection.delete_many({})
