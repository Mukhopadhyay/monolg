from datetime import datetime
from typing import Optional, Any


class Schema:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} object @ {hex(id(self))}"

    def to_dict(self) -> str:
        return self.__dict__


class Base(Schema):
    def __init__(self, name: str, message: str, time: datetime, level: str, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level=level, data=data, **kwargs)


class Info(Base):
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="info", data=data, **kwargs)


class Warning(Base):
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="warning", data=data, **kwargs)


class Error(Base):
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="error", data=data, **kwargs)


class Critical(Base):
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="critical", data=data, **kwargs)
