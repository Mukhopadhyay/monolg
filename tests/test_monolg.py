"""Tests for the main `Monolg` class"""

import pytest
from monolg import mongo_log


def test_possible_levels():
    for l in mongo_log.POSSIBLE_LEVELS:
        assert l in ('info', 'warning', 'error', 'critical')

