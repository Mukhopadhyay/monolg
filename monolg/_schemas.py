"""
Schema classes used in the project
"""

from datetime import datetime
from typing import Optional, Any, Dict


class Schema:
    """The base Schema class, creates instance attributes
    based on the kwargs in Runtime, which is why we can
    allow putting any key in the logging methods
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} object @ {hex(id(self))}"

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class Base(Schema):
    """The Base class this puts the must have kwargs in parent i.e., Schema
    """
    def __init__(self, name: str, message: str, time: datetime, level: str, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level=level, data=data, **kwargs)


class Info(Base):
    """The info schema class, level = 'info'
    """
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="info", data=data, **kwargs)


class Warning(Base):
    """The warning schema class, level = 'warning'
    """
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="warning", data=data, **kwargs)


class Error(Base):
    """The error schema class, level = 'error'
    """
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="error", data=data, **kwargs)


class Critical(Base):
    """The critical schema class, level = 'critical'
    """
    def __init__(self, name: str, message: str, time: datetime, data: Optional[Any] = None, **kwargs):
        super().__init__(name=name, message=message, time=time, level="critical", data=data, **kwargs)
