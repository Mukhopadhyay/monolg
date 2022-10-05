"""
Utility methods, used around the project.
"""

from datetime import datetime
from typing import Union, Optional


def get_datetime(as_string: Optional[bool] = False, fmt: Optional[str] = None) -> Union[str, datetime]:
    dt = datetime.now()
    if as_string and fmt:
        return dt.strftime(fmt)
    return dt
