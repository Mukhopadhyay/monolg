"""Tests for the Monolg class when MongoDB is available"""

import pytest
import monolg
import pymongo


class TestMonolg:

    @pytest.mark.monolg
    @pytest.mark.available
    def test_connect_monolg(self):
        """
        Case: Connecting the Monolg instance to the running MongoDB
        Precondition: MongoDB should be available on localhost:27017
        """
        mlg = monolg.Monolg()           # Monolg instance
        client = pymongo.MongoClient()  # PyMongo intance for checking the logs
        # Try to establish connection
        mlg.connect()
        # Check that the connected flag is True
        assert mlg.connected
        assert mlg.sys_connected

        # Check if the system logs went through
        monolg_db = client.Monolg
        logs_collection = monolg_db['Logs']
        sys_logs_collection = monolg_db['__monolg']

