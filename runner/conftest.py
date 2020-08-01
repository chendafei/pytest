import pytest
import yaml
import os
import pytest
from py._xmlgen import html
import os, sys
sys.path.append(os.getcwd())
from runner.test_run import TestInTheaters
import json
import requests
import jsonpath
import random
from utils.getData import get_all_test_datas_extract


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
        json={"account": "flychen1111+test001@gmail.com", "login_password": "123456"}
    )
    try:
        operate_token = before.json()['data']['operate_token']
        sign_in_log_id = before.json()['data']['sign_in_log_id']
    except KeyError:
        print('登录接口报错！接口值获取不到')
    return operate_token, sign_in_log_id


@pytest.fixture(scope="session")
def get_token():
    operate_token, sign_in_log_id = before_login()
    code = random.randrange(11111, 99999)
    dict1 = {"operate_token": operate_token,
             "sign_in_log_id": sign_in_log_id,
             "account": "flychen1111+test001@gmail.com",
             "login_password": "123456",
             "totp_captcha": {"validate_code": code, "sequence": ""}}
    r = requests.post(
        url='http://test2.coinex.com/res/user/sign/in/verify?X-CSRF-TOKEN=V_1VKTkN ',
        json=dict1)
    try:
        assert r.status_code == 200
        assert r.json()['code'] == 0
        return r.json()['data']['token']
    except KeyError:
        print('登录接口报错了，后面的用例不用执行了')


@pytest.fixture(scope="function", params=get_all_test_datas_extract("/Users/mac/PycharmProjects/pytest/testcases/"))
def gentrates_test_data(request):
    list_params, case = request.param
    if TestInTheaters.output:
        print(TestInTheaters.output)
        list_params = json.dumps(list_params)
        for key, value in TestInTheaters.output.items():
            list_params = list_params.replace(f'${key}', str(value))
        list_params = json.loads(list_params)
    return list_params


def pytest_generate_tests(metafunc):
    ids = []
    test_data = get_all_test_datas_extract("/Users/mac/PycharmProjects/pytest/testcases")
    if "parameters" in metafunc.fixturenames:
        for data in test_data:  # 用test_data中的id作为测试用例名称
            ids.append(data[0])

        metafunc.parametrize("parameters", test_data, ids=ids, scope="function")  # 用test_data这个列表对parameters进行参数化。

