import pytest
import yaml
import os
import pytest
from py._xmlgen import html
import os, sys
sys.path.append(os.getcwd())
from utils.commlib import get_all_test_datas_extract
from tests.test_add_api import TestInTheaters
import json
import logging

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")

@pytest.fixture(scope="session")
def env(request):
    config_path = os.path.join(request.config.rootdir,
                               "config",
                               "test2",
                               "config.yaml")
    with open(config_path) as f:
        env_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    return env_config


@pytest.fixture(scope="function", params=get_all_test_datas_extract("/Users/mac/PycharmProjects/pytest/testcases/API-Manager/delete_api.yaml"))
def gentrates_test_data(request):
    list_params = request.param
    if TestInTheaters.output:
        data = json.dumps(list_params)
        for key, value in TestInTheaters.output.items():
            print(key)
            print(value)
            list_params = data.replace(f'${key}', str(value))
        list_params = json.loads(list_params)
    return list_params





