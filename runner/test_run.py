import pytest
import os,sys
sys.path.append(os.getcwd())
import requests
import yamlpy
import jsonpath
import allure
from utils.assetValue import Tools
from utils.getData import get_all_test_datas, get_all_test_datas_extract
import json


@allure.feature('接口测试')
class TestInTheaters(Tools):

    @allure.story('登录')
    def test_login(self, get_token):
        TestInTheaters.output['token'] = get_token

    cases, parameters = get_all_test_datas("/Users/mac/PycharmProjects/pytest/testcases/singleCase")
    list_params = list(parameters)

    # 完整的单接口测试框架，无依赖关系的用例可通过该函数执行
    @pytest.mark.skip(reason='暂不需要')
    @pytest.mark.parametrize("case,http,expected", list_params, ids=cases)
    def test_run_single(self, env, case, http, expected):
        host = env['hosts']['test2']
        url = host+http.pop('url')
        method = http.pop('method')
        resp_obj = requests.request(method, url, **http)
        assert resp_obj.status_code == expected['status_code']
        self.asset_value(resp_obj, expected['response'])

    # 多接口测试框架，可以直接更新用例的值，但是不能展示用例名称
    @pytest.mark.skip('测试中，暂不需要')
    @allure.feature('接口测试')
    def test_run_combina(self, env, gentrates_test_data):
        case = gentrates_test_data[0]  # 测试用例标题
        request = gentrates_test_data[1]  # 测试请求数据
        expect = gentrates_test_data[2]  # 期望值
        extract = gentrates_test_data[3]  # 接口输出值
        allure.dynamic.story(case)
        with allure.step('获取测试数据'):
            host = env['hosts']['test2']
            url = host + request.pop('url')
            method = request.pop('method')
        with allure.step('请求接口'):
            resp_obj = requests.request(method, url, **request)
        with allure.step('获取输出值'):
            if extract:
                for key, value in extract.items():
                    TestInTheaters.output[key] = jsonpath.jsonpath(resp_obj.json(), value)[0]
        with allure.step('比对结果'):
            assert resp_obj.status_code == expect['status_code']
            self.asset_value(resp_obj, expect['response'])

    # 多接口测试框架，可以实时更新用例
    def test_data_driven(self, parameters, env):
        parameters = self.update_parameter(parameters)  # 更新用例
        case = parameters[0]  # 测试用例标题
        request = parameters[1]  # 测试请求数据
        expect = parameters[2]  # 期望值
        extract = parameters[3]  # 接口输出值
        allure.dynamic.story(case)
        with allure.step('获取测试数据'):
            host = env['hosts']['test2']
            url = host + request.pop('url')
            method = request.pop('method')
        with allure.step('请求接口'):
            resp_obj = requests.request(method, url, **request)
        with allure.step('获取输出值'):
            if extract:
                for key, value in extract.items():
                    TestInTheaters.output[key] = jsonpath.jsonpath(resp_obj.json(), value)[0]
        with allure.step('比对结果'):
            assert resp_obj.status_code == expect['status_code']
            self.asset_value(resp_obj, expect['response'])

