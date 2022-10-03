import pytest


@pytest.fixture
def schema_to_dict():
    return [({}, {}), ({"a": 1}, {"a": 1}), ({"a": 3 + 1j}, {"a": 3 + 1j})]
