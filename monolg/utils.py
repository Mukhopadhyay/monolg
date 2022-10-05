"""
Utility methods, used around the project.
"""

from datetime import datetime
from typing import Union, Optional

def get_datetime(fmt: Optional[str] = None) -> Union[str, datetime]:
    dt = datetime.now()
    if fmt:
        return dt.strftime(fmt)
    return dt
