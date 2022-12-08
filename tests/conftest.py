"""Pytest fixtures"""

import pytest
from typing import Tuple, Dict
import datetime


@pytest.fixture
def schema_to_dict():
    return [({}, {}), ({"a": 1}, {"a": 1}), ({"a": 3 + 1j}, {"a": 3 + 1j})]


@pytest.fixture
def config_sections() -> Tuple[str, str, str]:
    return ("DEFAULT", "SETTINGS", "MONGO")


@pytest.fixture
def config_keys() -> Tuple[Dict[str, tuple]]:
    return (
        {"DEFAULT": ("PROJECT_NAME", "PROJECT_VERSION", "AUTHOR_NAME", "AUTHOR_EMAIL")},
        {"SETTINGS": ("DT_FMT", "LEVEL")},
        {"MONGO": ("HOST", "PORT", "DEFAULT_COLLECTION_NAME", "TIMEOUT")},
    )


@pytest.fixture
def test_integer_keys():
    return [
        (
            "MONGO",
            "PORT",
        ),
        ("MONGO", "TIMEOUT"),
    ]


@pytest.fixture
def test_get_dt_types():
    return [
        # Kwargs, return_type
        ({}, datetime.datetime),
        ({"as_string": True}, str),
        ({"fmt": "%d-%m-%Y"}, datetime.datetime),
        ({"as_string": True, "fmt": "%d-%m-%Y"}, str),
    ]


@pytest.fixture
def possible_levels():
    return ["info", "warning", "error", "critical"]
