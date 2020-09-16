import os
from configparser import ConfigParser

import pytest
import requests


def pytest_configure(config):
    config_ini = ConfigParser()
    config_ini.read(os.path.join(config.rootdir, "tests", "config.ini"))

    config.option.base_url = config_ini.get(section='ENV_SETTINGS',
                                            option='base_url')


@pytest.fixture(scope='session')
def send_request(pytestconfig):
    def _request(method='GET', endpoint='/', payload=None, headers=None):
        if method == 'GET':
            return requests.get(
                url=f"{pytestconfig.getoption('base_url')}{endpoint}")
        elif method == 'POST':
            return requests.post(
                url=f"{pytestconfig.getoption('base_url')}{endpoint}",
                json=payload,
                headers=headers,
            )
        elif method == "DELETE":
            return requests.delete(
                url=f"{pytestconfig.getoption('base_url')}{endpoint}")
    return _request
