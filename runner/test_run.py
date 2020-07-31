import pytest
import os,sys
sys.path.append(os.getcwd())
import requests
import yamlpy
import jsonpath
import allure
from utils.assertValue.Tools
from utils.getData.get_all_test_datas


@allure.feature('API密钥功能')
class TestInTheaters(Tools):
    output = {}

    @allure.feature('登录')
    def test_login(self, get_token):
        TestInTheaters.output['token'] = get_token

    cases, parameters = get_all_test_datas("/Users/mac/PycharmProjects/pytest/testcases/singleCase")
    list_params = list(parameters)

    # 完整的单接口测试框架
    @pytest.mark.skip(reason='暂不需要')
    # @pytest.mark.parametrize("case,http,expected", list_params, ids=cases)
    def test_run_single(self, env, case, http, expected):
        host = env['hosts']['test2']
        url = host+http.pop('url')
        method = http.pop('method')
        resp_obj = requests.request(method, url, **http)
        assert resp_obj.status_code == expected['status_code']
        self.asset_value(resp_obj, expected['response'])

    # 多接口测试框架
    @allure.story('接口测试')
    def test_run_combina(self, env, gentrates_test_data):
        case = gentrates_test_data[0]  # 测试用例标题
        request = gentrates_test_data[1]  # 测试请求数据
        expect = gentrates_test_data[2]  # 期望值
        extract = gentrates_test_data[3]  # 接口输出值
        allure.story(case)
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




