"""
Tests for the monolg/configs.ini file
"""

import os
import pytest
from configparser import RawConfigParser


class TestConfigINI:
    """
    Tests the configs.ini file
    """
    config_path = "../monolg/monolg/configs.ini"
    config = RawConfigParser()
    config.read(config_path)

    @pytest.mark.configs
    def test_config_exit(self):
        assert os.path.exists(os.path.abspath(self.config_path))

    @pytest.mark.configs
    def test_for_necessary_sections(self, config_sections):
        config_sections = [x[0] for x in list(self.config.items())]
        for section in config_sections:
            assert section in config_sections

    @pytest.mark.configs
    def test_for_necessary_keys(self, config_keys):
        for d in config_keys:
            for section_name, key_names in d.items():
                keys = [x[0] for x in self.config.items(section_name)]
                for key_name in key_names:
                    assert key_name.casefold() in keys

    @pytest.mark.configs
    def test_integer_keys(self, test_integer_keys):
        for sec, k in test_integer_keys:
            assert self.config[sec][k].isnumeric()
