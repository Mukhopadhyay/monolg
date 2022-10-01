from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Base:
    """Base schema class"""

    name: str
    message: str
    time: datetime
    level: str
    data: Optional[Any] = {}


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
