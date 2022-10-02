from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Base:
    """Base schema class"""

    name: str
    message: str
    time: datetime
    level: str
    data: Optional[Any] = field(default_factory=dict)


@dataclass
class Info(Base):
    level: str = "info"


@dataclass
class Warning(Base):
    level: str = "warning"


@dataclass
class Error(Base):
    error_class: str
    level: str = "error"


@dataclass
class Critical(Base):
    level: str = "critical"
