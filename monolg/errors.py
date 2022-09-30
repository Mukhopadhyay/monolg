"""Script containing the exceptions"""


class Error(Exception):
    pass


class ConnectionNotEstablishedErr(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __str__(self) -> str:
        return "Connection not established!"

    def __repr__(self) -> str:
        return "Connection not established!"
