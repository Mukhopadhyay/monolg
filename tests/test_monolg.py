"""Tests for the Monolg class when MongoDB is available"""

import pytest
import monolg
import pymongo


class TestMonolg:

    @pytest.mark.monolg
    def test_normal_instantiation_and_conn(self):
        mlg = monolg.Monolg()
        client = pymongo.MongoClient()
        # Try to establish connection
        mlg.connect()
        # Check that the connected flag is True
        assert mlg.connected
