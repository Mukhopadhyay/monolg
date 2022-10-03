"""
Tests for the schema classes present in _schemas.py
"""

import pytest
from monolg import _schemas


class TestSchemaClass:
    @pytest.mark.schema
    def test_instantiation(self):
        s = _schemas.Schema()
        assert s

    @pytest.mark.schema
    def test_attribute_presence(self):
        s = _schemas.Schema(a=1, b="1")
        assert s.a == 1
        assert s.b == "1"

    @pytest.mark.schema
    def test_str_casting(self):
        s = _schemas.Schema(message="Something")
        assert str(s).startswith("Schema object @ ")

    @pytest.mark.schema
    def test_abs_message_str_casting(self):
        s = _schemas.Schema()
        s.counter = 0
        assert isinstance(str(s), str)  # Shouldn't raise errors
        assert str(s).startswith("Schema object @ ")

    @pytest.mark.schema
    def test_schema_to_dict(self, schema_to_dict):
        for args, ret in schema_to_dict:
            s = _schemas.Schema(**args)
            assert s.to_dict() == ret
