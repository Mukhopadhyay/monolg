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
from monolg.errors import (ConnectionNotEstablishedErr,
                           InvalidLevelWarning,
                           NotConnectedWarning)

# Setting up the global configss
config = RawConfigParser()
config.read(os.path.join("monolg", "configs.ini"))


POSSIBLE_LEVELS = ("info", "warning", "error", "critical")


class Monolg(object):

    # Default mongo settings
    # If None if found on the kwargs of the constructor
    # These values will be used instead.
    HOST: str = config["MONGO"]["HOST"]
    PORT: int = int(config["MONGO"]["PORT"])
    TIMEOUT: int = int(config["MONGO"]["TIMEOUT"])

    # Default logger settings
    NAME: str = config["DEFAULT"]["PROJECT_NAME"].capitalize()
    LEVEL: str = config["SETTINGS"]["LEVEL"]
    DT_FMT: str = config['SETTINGS']['DT_FMT']

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
        **kwargs,
    ) -> None:
        self.host: Optional[str] = host
        if not self.host:
            self.host = self.HOST

        self.port: Optional[int] = port
        if not self.port:
            self.port = self.PORT

        self.name: Optional[str] = name
        if not self.name:
            self.name = self.NAME

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

        self.verbose = verbose

        # Following will be populated after .connect() is invoked
        self.db: pymongo.database.Database = None
        self.collection: pymongo.collection.Collection = None

        # These will be populated later
        self.db_name = None
        self.collection_name = None

        # Is this instance connected to Mongo??
        self.__connected = False

        self.client: pymongo.MongoClient = client
        if not self.client:
            self.client = pymongo.MongoClient(
                host=self.host,
                port=self.port,
                serverSelectionTimeoutMS=self.serv_sel_timeout
            )

    @classmethod
    def from_connection(cls, client: pymongo.MongoClient) -> object:
        # TODO: If this is how its instantiated
        # then the connection cannot be reopened
        return cls(client=client)

    def __test_connection(self) -> None:
        try:
            # Test out a connection
            __test_client: pymongo.MongoClient = pymongo.MongoClient(
                self.host,
                self.port,
                serverSelectionTimeoutMS=self.serv_sel_timeout
            )
            __test_client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            # This is more confusing then it is helpful
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
        self.__connected = True

    def reopen(self) -> None:
        """Reopens the network, reinitializes the MongoClient"""
        self.client = pymongo.MongoClient(
            host=self.host, port=self.port, serverSelectionTimeoutMS=self.serv_sel_timeout
        )
        self.connect(self.db_name, self.collection_name)

    def close(self) -> None:
        """Closes connection
        Read more here:
        https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient.close

        A connection pool still keeps running, so if we perform some op this
        connection will be re-opened.
        https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        """
        if self.__connected:
            self.client.close()
            self.__connected = False

    def __insert_model(self, level: str, **kwargs) -> None:
        model = self.SCHEMA.get(level)
        if not model:
            msg = f"Invalid level '{level}' logging on info instead. Use one of {POSSIBLE_LEVELS}"
            warnings.warn(msg, category=InvalidLevelWarning)
            model = self.SCHEMA.get('info')
        # Instantiate the schema model based on the keyword arguments
        log_model = model(**kwargs)
        # Insert into mongo
        self.collection.insert_one(log_model.to_dict())

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

        self.__insert_model(
            level, name=name if name else self.name, message=message, time=dt, data=data,
            file=self.filename, **kwargs
        )
        if self.verbose and verbose:
            utils.print_log(dt, message, level.upper())

    def info(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = {}, **kwargs) -> None:
        self.log(message, name, "info", data, **kwargs)

    def warning(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = {}, **kwargs) -> None:
        self.log(message, name, "warning", data, **kwargs)

    def error(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = {}, **kwargs) -> None:
        self.log(message, name, "error", data, **kwargs)

    def critical(self, message: str, name: Optional[str] = None, data: Optional[Dict[str, Any]] = {}, **kwargs) -> None:
        self.log(message, name, "critical", data, **kwargs)

    def clear_logs(self) -> None:
        if not self.__connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)
        self.collection.delete_many({})
        print("All logs removed!")
