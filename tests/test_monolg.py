"""Tests for the Monolg class when MongoDB is available"""

import bson
import pytest
import monolg
import pymongo
from pymongo.collection import Collection
from typing import Optional, Tuple


class TestMonolg:

    client: pymongo.MongoClient = None
    db: pymongo.MongoClient = None

    def get_collections(
        self, db: Optional[str] = None, log_collection: Optional[str] = None, system_collection: Optional[str] = None
    ) -> Tuple[Collection, Collection]:
        self.client = pymongo.MongoClient()
        if not db:
            db = "Monolg"
        if not log_collection:
            log_collection = "Logs"
        if not system_collection:
            system_collection = "__monolg"
        self.db = self.client[db]
        return self.db[log_collection], self.db[system_collection]

    @pytest.mark.monolg
    @pytest.mark.available
    def test_default_sys_logs(self):
        """
        Case: Connecting the Monolg instance to the running MongoDB
        Precondition: MongoDB should be available on localhost:27017
        """
        mlg = monolg.Monolg()  # Monolg instance

        # Clearing the collections
        logs, system = self.get_collections()
        logs.delete_many({})
        system.delete_many({})

        mlg.connect()  # Try to establish connection

        assert mlg.connected  # Default logs collection should be connected
        assert mlg.sys_connected  # System logs collection should be connected

        mlg.close()  # Close the connection

        # ----------------------------------------------------
        # Check whatever we're putting in Mongo is right
        # ----------------------------------------------------
        sys_logs = list(system.find({}))

        assert len(sys_logs) == 2  # There should be 2 logs, open and close

        for l in sys_logs:
            assert l["name"] == "system"
            assert isinstance(l["_id"], bson.ObjectId)
            assert l["level"] == "info"

        assert sys_logs[0]["message"] == "monolg connected to mongodb"
        assert sys_logs[0]["data"]["database"] == "Monolg"
        assert sys_logs[0]["data"]["collection"] == "Logs"

        assert sys_logs[1]["message"] == "monolg connection with mongodb closed"

        self.client.close()

    @pytest.mark.monolg
    @pytest.mark.available
    def test_sys_log_disabled(self):
        """
        Case: Connecting the Monolg instance to the running MongoDB with sys_log set to False
        Precondition: MongoDB should be available on localhost:27017
        """
        mlg = monolg.Monolg(system_log=False)  # Monolg instance

        # Clearing the collections
        logs, system = self.get_collections()
        logs.delete_many({})
        system.delete_many({})

        mlg.connect()  # Try to establish connection

        assert mlg.connected  # Default logs collection should be connected
        assert not mlg.sys_connected  # System logs collection should be connected

        mlg.close()  # Close the connection

        # ----------------------------------------------------
        # Check that we're putting nothing in monolg
        # ----------------------------------------------------
        sys_logs = list(system.find({}))

        assert len(sys_logs) == 0  # There should be 0 logs, open and close

        self.client.close()

    @pytest.mark.monolg
    @pytest.mark.available
    def test_sys_log_disabled(self):
        """
        Case: Connecting the Monolg instance to the running MongoDB with sys_log set to False
        Precondition: MongoDB should be available on localhost:27017
        """
        mlg = monolg.Monolg(system_log=False)  # Monolg instance

        # Clearing the collections
        logs, system = self.get_collections()
        logs.delete_many({})
        system.delete_many({})

        mlg.connect()  # Try to establish connection

        assert mlg.connected  # Default logs collection should be connected
        assert not mlg.sys_connected  # System logs collection should be connected

        mlg.close()  # Close the connection

        # ----------------------------------------------------
        # Check that we're putting nothing in monolg
        # ----------------------------------------------------
        sys_logs = list(system.find({}))

        assert len(sys_logs) == 0  # There should be 0 logs, open and close

        self.client.close()
