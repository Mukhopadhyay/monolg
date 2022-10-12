"""Tests for the main `Monolg` class"""

import monolg
import pytest
import pymongo
from monolg import mongo_log


def test_possible_levels():
    for l in mongo_log.POSSIBLE_LEVELS:
        assert l in ('info', 'warning', 'error', 'critical')


class TestMonolg:

    client = pymongo.MongoClient()

    def test_object():
        mlg = monolg.Monolg()
        for x in mlg.SCHEMA.keys():
            assert x in ('info', 'warning', 'error', 'critical')
