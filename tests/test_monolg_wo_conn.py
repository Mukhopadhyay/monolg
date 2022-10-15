"""Tests for the main `Monolg` class"""

import monolg
import pytest
import pymongo
from monolg import errors
from monolg import mongo_log
from monolg._schemas import Base


def test_possible_levels(possible_levels):
    for l in mongo_log.POSSIBLE_LEVELS:
        assert l in possible_levels


class TestMonolgDefaultProperties:
    mlg = monolg.Monolg()

    @pytest.mark.monolg
    def test_schema_mapping(self, possible_levels):
        for x in self.mlg.SCHEMA.keys():
            assert x in possible_levels
        for v in self.mlg.SCHEMA.values():
            assert issubclass(v, Base)

    @pytest.mark.monolg
    def test_default_values(self):
        assert self.mlg.HOST == "localhost"
        assert self.mlg.PORT == 27017
        assert self.mlg.TIMEOUT == 10000
        assert self.mlg.LEVEL == "info"
        assert self.mlg.NAME == "Monolg"
        assert self.mlg.DT_FMT == "%d-%m-%Y %H:%M:%S"

    @pytest.mark.monolg
    def test_default_instance_attributes(self):
        assert self.mlg.host == "localhost"
        assert self.mlg.port == 27017
        assert self.mlg.serv_sel_timeout == 10000
        assert self.mlg.level == "info"
        assert self.mlg.name == "Monolg"


class TestMonolgNonConnected:

    mlg = monolg.Monolg()

    @pytest.mark.monolg
    def test_non_connected_conn_flag(self):
        # Before connecting the connection should be false
        assert not self.mlg.connected

    @pytest.mark.monolg
    def test_non_connected_conn_time(self):
        assert not self.mlg.connection_time

    @pytest.mark.monolg
    def test_default_sys_log(self):
        # By default we should have system logs
        assert not self.mlg.sys_connected

    @pytest.mark.monolg
    def test_not_is_from_client(self):
        # By default we should have system logs
        assert not self.mlg.is_from_client

    @pytest.mark.monolg
    def test_clear_logs_before_conn(self):
        # Should warn NotConnectedWarning
        with pytest.warns(errors.NotConnectedWarning):
            self.mlg.clear_logs()

    @pytest.mark.monolg
    def test_clear_sys_logs_bef_conn(self):
        # Should warn NotConnectedWarning
        with pytest.warns(errors.NotConnectedWarning):
            self.mlg.clear_sys_logs()

    @pytest.mark.monolg
    def test_log_bef_conn(self):
        with pytest.raises(errors.NotConnectedError):
            self.mlg.log("...")

    @pytest.mark.monolg
    def test_non_conn_reopen(self):
        with pytest.raises(errors.ConnectionNotReopened):
            self.mlg.reopen()

    @pytest.mark.monolg
    def test_non_conn_close(self):
        # Trying to close the connection that isnt open
        # Shouldn't raise any errors
        assert not self.mlg.close()


class TestMonolgViaClient(TestMonolgNonConnected):

    client = pymongo.MongoClient()
    mlg = monolg.Monolg.from_client(client)

    @pytest.mark.monolg
    def test_not_is_from_client(self):
        # By default we should have system logs
        assert self.mlg.is_from_client

