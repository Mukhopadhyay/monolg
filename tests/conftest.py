import pytest


@pytest.fixture
def schema_to_dict():
    return [({}, {}), ({"a": 1}, {"a": 1}), ({"a": 3 + 1j}, {"a": 3 + 1j})]


@pytest.fixture
def config_sections():
    return ("DEFAULT", "SETTINGS", "MONGO")


@pytest.fixture
def config_keys():
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
