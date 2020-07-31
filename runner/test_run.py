import pytest
import requests
import os, sys
sys.path.append(os.getcwd())
import requests
import yamlpy
from utils.commlib import diff_response, asset_value, get_all_test_datas,get_all_test_datas_extract,get_test_data
import allure
import jsonpath

@allure.feature('API密钥功能')
class TestInTheaters(object):
    output = {}

    def test_login(self, get_token):
        TestInTheaters.output['token'] = get_token

    cases, parameters = get_all_test_datas("E://code/pytest/testcases/singleCase")
    list_params = list(parameters)
    # 完整的单接口测试框架
    @pytest.mark.skip(reason='暂不需要')
    @pytest.mark.parametrize("case,http,expected", list_params, ids=cases)
    def test_run_single(self, env, case, http, expected):
        host = env['hosts']['test2']
        url = host+http.pop('url')
        method = http.pop('method')
        resp_obj = requests.request(method, url, **http)
        assert resp_obj.status_code == expected['status_code']
        asset_value(resp_obj, expected['response'])

    # 多接口测试框架
    # @pytest.mark.parametrize("case,http,expected,extract", get_data, ids=cases)
    def test_run_combina(self, env, gentrates_test_data):
        host = env['hosts']['test2']
        url = host + gentrates_test_data[1].pop('url')
        method = gentrates_test_data[1].pop('method')
        resp_obj = requests.request(method, url, **gentrates_test_data[1])
        if gentrates_test_data[3]:
            for key, value in gentrates_test_data[3].items():
                TestInTheaters.output[key] = jsonpath.jsonpath(resp_obj.json(), value)[0]
        assert resp_obj.status_code == gentrates_test_data[2]['status_code']
        asset_value(resp_obj, gentrates_test_data[2]['response'])




