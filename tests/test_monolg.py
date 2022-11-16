"""Tests for the Monolg class when MongoDB is available"""

import pytest
import monolg
import pymongo


class TestMonolg:

    # Case: Test connecting monolg when MongoDB is unavailable with default params
    @pytest.mark.monolg
    @pytest.mark.unavailable
    def test_normal_instantiation_and_conn(self):
        mlg = monolg.Monolg()
        client = pymongo.MongoClient()
        # Try to establish connection
        mlg.connect()
        # Check that the connected flag is True
        assert mlg.connected
        assert mlg.sys_connected

        # Check if the system logs went through

    # Case: Test connecting monolg when MongoDB is available with default params

    # Case: Test connecting monolg when MongoDB is unavailable with connection string

    # Case: Test connecting monolg when MongoDB is available with connection string
