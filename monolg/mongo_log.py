"""
        Main script containing the classes
"""
# Built-in modules
import os
import warnings
from configparser import ConfigParser
from datetime import datetime
from typing import Optional, Dict, Any

# Third-party
import pymongo

# Custom modules
from monolg import utils
from monolg import _schemas
from monolg.errors import ConnectionNotEstablishedErr, InvalidLevelWarning, NotConnectedWarning

# Setting up the global configss
config = ConfigParser()
config.read(os.path.join("monolg", "configs.ini"))


POSSIBLE_LEVELS = ("info", "warning", "error", "critical")


class Monolg(object):

    # Default mongo settings
    # If None if found on the kwargs of the constructor
    # These values will be used instead.
    HOST: str = config["MONGO"]["HOST"]
    PORT: int = int(config["MONGO"]["PORT"])
    TIMEOUT: int = config["MONGO"]["TIMEOUT"]

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
        verbose: Optional[bool] = False,  # prints the logging statement in stdout
        **kwargs,
    ) -> None:
        self.host = host
        if not self.host:
            self.host = self.HOST
            
        self.port = port
        if not self.port:
            self.port = self.PORT
            
        self.name = name
        if not self.name:
            self.name = self.NAME

        self.level = level
        if not self.level:
            self.level = self.LEVEL

        self.serv_sel_timeout = serv_sel_timeout
        if not serv_sel_timeout:
            self.serv_sel_timeout = self.TIMEOUT

        self.filename = None
        try:
            self.filename = __file__
        except NameError:  # This is for notebooks
            pass

        self.verbose = verbose

        # Following will be populated after .connect() is invoked
        self.db = None
        self.collection = None

        # Is this instance connected to Mongo??
        self.__connected = False

        self._server_sel_timeout_ms = kwargs.pop("serv_sel_timeout", self.TIMEOUT)

        if not kwargs.get("client", None):
            self.client = pymongo.MongoClient(
                host=self.host, port=self.port, serverSelectionTimeoutMS=self._server_sel_timeout_ms
            )
        else:
            self.client = kwargs.get("client")

    @classmethod
    def from_connection(cls, client: pymongo.MongoClient) -> object:
        return cls(client=client)

    def __test_connection(self) -> None:
        try:
            # Test out a connection
            __test_client = pymongo.MongoClient(
                self.host, self.port, serverSelectionTimeoutMS=self._server_sel_timeout_ms
            )
            __test_client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as conn_err:
            # This is more confusing then it is helpful
            raise ConnectionNotEstablishedErr()

    def connect(self, db: Optional[str] = None, collection: Optional[str] = None) -> None:
        if not db:
            db = self.DEFAULT_DB_NAME
        if not collection:
            collection = self.DEFFAULT_COLLECTION_NAME
        self.__test_connection()
        self.db: pymongo.database.Database = self.client.get_database(db)
        self.collection: pymongo.collection.Collection = self.db.get_collection(collection)
        self.__connected = True

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

    def __insert_model(self, level: str, **kwargs) -> None:
        model = self.SCHEMA.get(level)
        if not model:
            msg = f"Invalid level '{level}' logging on info instead. Use one of {POSSIBLE_LEVELS}"
            warnings.warn(msg, category=InvalidLevelWarning)
        # Instantiate the schema model based on the keyword arguments
        log_model = model(**kwargs)
        # Insert into mongo
        self.collection.insert_one(log_model.to_dict())

    def log(
        self,
        message: str,
        name: Optional[str] = None,
        level: Optional[str] = None,
        data: Optional[Dict[str, Any]] = {},
        datetime_as_string: Optional[bool] = False,  # Defaults to setting it as datetime objects
        datetime_fmt: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        error_class: str        | In kwargs
        """
        if not self.__connected:
            msg = "Monolg instance is not connected, Please do object.connect() first!"
            warnings.warn(msg, category=NotConnectedWarning)
        if not level:
            level = self.level
        
        fmt = datetime_fmt
        if not fmt:
            fmt = self.DT_FMT
        
        dt = utils.get_datetime(datetime_as_string, fmt)
        
        self.__insert_model(
            level, name=name if name else self.name, message=message, time=dt, data=data, **kwargs
        )
        if self.verbose:
            stdout = f'{dt} {message}'
            print(stdout)

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
