"""Script containing the exceptions"""


class Error(Exception):
    pass


class ConnectionNotEstablishedErr(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __str__(self) -> str:
        return "Connection not established!"


class NotConnectedWarning(Error, Warning):
    def __init__(self, message: str, **kwargs) -> None:
        self.message = message
        super().__init__(self, message, **kwargs)

    def __str__(self) -> str:
        return self.message


class InvalidLevel(Error, Warning):
    def __init__(self, message: str, **kwargs) -> None:
        self.message = message
        super().__init__(self, message, **kwargs)

    def __str__(self) -> str:
        return self.message
