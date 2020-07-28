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
    @allure.story('删除API功能')
    @pytest.mark.skip(reason='暂时不需要用')
    @pytest.mark.parametrize('auth', [200,201])
    def test_delete_api(self, auth):
        print(auth)
        auth = str(auth)
        url = 'http://test3.coinex.com/res/user/auth/api/{}?X-CSRF-TOKEN=Co3-kzrn'.format(auth)
        header = {
            "Content-Type": "application/json",
            "Authorization": "535B2845C194402E8DA9CA3E0FDBD0A7",
            "Accept-Language": "zh_Hans_CN",
            "Content-Type": "application/json;charset=UTF-8"
        }
        params = {
            "totp_captcha":{"validate_code":"777777", "sequence":""}
        }

        re = requests.delete(url, headers=header, json=params)
        assert re.json()['code'] == 0

    # cases, parameters = get_all_test_datas("E://code/pytest/testcases")
    # list_params = list(parameters)
    cases, parameters = get_test_data("E://code/pytest/testcases/API-Manager/add_api.yaml")
    list_params = list(parameters)

    # 完整的单接口测试框架
    @pytest.mark.skip(reason='暂不执行')
    @pytest.mark.parametrize("case,http,expected", list_params, ids=cases)
    def test_run(self, env, case, http, expected):
        host = env['hosts']['test2']
        url = host+http.pop('url')
        method = http.pop('method')
        resp_obj = requests.request(method, url, **http)
        assert resp_obj.status_code == expected['status_code']
        asset_value(resp_obj, expected['response'])

    cases, parameters = get_all_test_datas_extract("E://code/pytest/testcases/API-Manager/delete_api.yaml")
    list_params = list(parameters)

    # 多接口测试框架
    # @pytest.mark.parametrize("case,http,expected,extract", get_data, ids=cases)
    def test_run(self, env, gentrates_test_data):
        host = env['hosts']['test2']
        url = host + gentrates_test_data[1].pop('url')
        method = gentrates_test_data[1].pop('method')
        resp_obj = requests.request(method, url, **gentrates_test_data[1])
        if gentrates_test_data[3]:
            for key, value in gentrates_test_data[3].items():
                TestInTheaters.output[key] = jsonpath.jsonpath(resp_obj.json(), value)
        assert resp_obj.status_code == gentrates_test_data[2]['status_code']
        asset_value(resp_obj, gentrates_test_data[2]['response'])




