"""Tests for the utility script, i.e., monolg/utils.py"""

import pytest
import datetime
from monolg import utils


@pytest.mark.utils
def test_get_datetime(test_get_dt_types):
    for kwargs, obj in test_get_dt_types:
        isinstance(utils.get_datetime(**kwargs), obj)


@pytest.mark.utils
def test_get_datetime_values():
    # Test that the format is being used
    d = utils.get_datetime(as_string=True, fmt="%d-%m-%Y")
    assert datetime.datetime.strptime(d, "%d-%m-%Y")
    # Test that the 'dt' param is working
    x = datetime.datetime(2022, 1, 1, 10, 10, 0)
    d = utils.get_datetime(dt=x)
    # Test the string formatting is correct
    d = utils.get_datetime(as_string=True, fmt="%d-%m-%Y %H:%M:%S", dt=x)
    assert d == "01-01-2022 10:10:00"
