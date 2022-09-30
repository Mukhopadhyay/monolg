from datetime import datetime
from dataclasses import dataclass


@dataclass
class Base:
    """Base schema class"""

    name: str
    time: datetime
    level: str


@dataclass
class Info(Base):
    level: str = "info"


@dataclass
class Warning(Base):
    level: str = "warning"


@dataclass
class Error(Base):
    level: str = "error"


@dataclass
class Critical(Base):
    level: str = "critical"
