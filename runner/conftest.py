import pytest
import yaml
import os
import pytest
from py._xmlgen import html
import os, sys
sys.path.append(os.getcwd())
from utils.commlib import get_all_test_datas_extract,get_test_data,asset_value
from runner.test_run import TestInTheaters
import json
import requests
import jsonpath
import random

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


def before_login():
    before = requests.post(
        url="http://test2.coinex.com/res/user/sign/in?X-CSRF-TOKEN=vrCF7aT8",
        json={"account": "flychen1111+test002@gmail.com", "login_password": "123456"}
    )
    operate_token = before.json()['data']['operate_token']
    sign_in_log_id = before.json()['data']['sign_in_log_id']
    return operate_token, sign_in_log_id


@pytest.fixture(scope="session")
def get_token():
    operate_token, sign_in_log_id = before_login()
    code = random.randrange(11111, 99999)
    dict1 = {"operate_token": operate_token,
             "sign_in_log_id": sign_in_log_id,
             "account": "flychen1111+test002@gmail.com",
             "login_password": "123456",
             "totp_captcha": {"validate_code": code, "sequence": ""}}
    r = requests.post(
        url='http://test2.coinex.com/res/user/sign/in/verify?X-CSRF-TOKEN=V_1VKTkN ',
        json=dict1)
    return r.json()['data']['token']


@pytest.fixture(scope="function", params=get_all_test_datas_extract("E://code/pytest/testcases/combinCase"))
def gentrates_test_data(request):
    list_params = request.param
    if TestInTheaters.output:
        print(TestInTheaters.output)
        data = json.dumps(list_params)
        for key, value in TestInTheaters.output.items():
            list_params = data.replace(f'${key}', str(value))
        list_params = json.loads(list_params)
        print(list_params)
    return list_params







