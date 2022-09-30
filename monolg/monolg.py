"""
        Main script containing the classes
"""
import pymongo
from pymongo.errors import ConnectionNotEstablishedErr
from typing import Optional


class Monolg(object):

    HOST: str = "localhost"
    PORT: int = 27017

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, **kwargs) -> None:
        self.host = host
        if not self.host:
            self.host = self.HOST
        self.port = port
        if not self.port:
            self.port = self.PORT

        self._server_sel_timeout_ms = kwargs.pop("serv_sel_timeout", 1000)

        # Test out a connection
        __test_client = pymongo.MongoClient(self.host, self.port, serverSelectionTimeoutMS=100)
        try:
            __test_client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            raise ConnectionNotEstablishedErr("something")

        self.client = pymongo.MongoClient(
            host=self.host, port=self.port, serverSelectionTimeoutMS=self._server_sel_timeout_ms
        )
