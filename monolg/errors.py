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
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message


class InvalidLevelWarning(Error, Warning):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message


class ConnectionNotReopened(Error):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message
