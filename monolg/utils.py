"""
Utility methods, used around the project.
"""

from colorama import Fore, init
from datetime import datetime
from typing import Union, Optional

init(autoreset=True)

color_map = {"INFO": Fore.GREEN, "WARNING": Fore.YELLOW, "ERROR": Fore.MAGENTA, "CRITICAL": Fore.RED}


def get_datetime(
    as_string: Optional[bool] = False, fmt: Optional[str] = None, dt: Optional[datetime] = None
) -> Union[str, datetime]:
    """Returns datetime as either string or python datetime object

    Args:
        as_string (Optional[bool], optional): Whether to return as string or not. Defaults to False.
        fmt (Optional[str], optional): If as_string is set to True, what format should be used. Any datetime.strftime() compatible formt works. Defaults to None.
        dt (Optional[datetime], optional): datetime object that is to be formatted. Defaults to None.

    Returns:
        Union[str, datetime]: _description_
    """
    dt = dt
    if not dt:
        dt = datetime.now()
    if as_string and fmt:
        return dt.strftime(fmt)
    return dt


def print_log(dt: Union[datetime, str], message: str, level: str, name: str, fmt: Optional[str] = None) -> None:
    """Generates & prints the logging message at STDOUT.

    Args:
        dt (Union[datetime, str]): datetime object used by the logger.
        message (str): The message that is being logged.
        level (str): Level of this log. Based on these values we're going to color code the level string.
        name (str): Name used for this log statement.
        fmt (Optional[str], optional): format string for the datetime object. Defaults to None.
    """
    if fmt:
        dt = dt.strftime(fmt)
    color = color_map.get(level, Fore.GREEN)
    head = f"{dt} [{color}{level}]"
    print(head, f"[{name}] {message}")
