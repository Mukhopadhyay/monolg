"""
        Main script containing the classes
"""
# Built-in modules
from typing import Optional

# Third-party
import pymongo

# Custom modules
from monolg.errors import ConnectionNotEstablishedErr


class Monolg(object):

    HOST: str = "localhost"
    PORT: int = 27017
    NAME: str = "monolg"
    LEVEL: str = "info"
    TIMEOUT: int = 10000

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        name: Optional[str] = None,
        level: Optional[str] = LEVEL,
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

        self.filename = None
        try:
            self.filename = __file__
        except NameError:  # This is for notebooks
            pass

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

    def connect(self, db: str, collection: str) -> None:
        self.__test_connection()
        self.db: pymongo.database.Database = self.client.get_database(db)
        self.collection: pymongo.collection.Collection = self.db.get_collection(collection)
        self.__connected = True

    def log(self) -> None:
        if not self.__connected:
            print("Instance is not connected to Mongo!")
