"""Script containing the exceptions"""


class Error(Exception):
    pass


class ConnectionNotEstablishedErr(Error):
    """Gets raised if we cannot establish connection with Mongo
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __str__(self) -> str:
        return "Connection not established!"


class NotConnectedWarning(Error, Warning):
    """Gets raised if we're trying to perform some operation on the collection
    but the instance is not connected.
    """
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message


class InvalidLevelWarning(Error, Warning):
    """This warning is given if given level while logging is not with
    permissible values (info, warning, error, critical)
    """
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message


class ConnectionNotReopened(Error):
    """This is raised when we're unable to re-establish mongodb connection
    """
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(self, message, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return self.message
