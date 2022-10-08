"""
Utility methods, used around the project.
"""

from colorama import Fore, init
from datetime import datetime
from typing import Union, Optional

init(autoreset=True)

color_map = {
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.MAGENTA,
    'CRITICAL': Fore.RED
}


def get_datetime(as_string: Optional[bool] = False, fmt: Optional[str] = None) -> Union[str, datetime]:
    dt = datetime.now()
    if as_string and fmt:
        return dt.strftime(fmt)
    return dt


def print_log(dt: Union[datetime, str], message: str, level: str, fmt: Optional[str] = None) -> None:
    if fmt:
        dt = dt.strftime(fmt)
    col = color_map.get(level, Fore.GREEN)
    head = f'{dt} {col}{level}'
    print(head, message)
