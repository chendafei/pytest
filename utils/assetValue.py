import requests
import jsonpath
import os, sys
sys.path.append(os.getcwd())
import json
import random


class Tools():
    output = {}   # 全局变量，用于存储接口的返回值
    '''
        下面的函数是响应结果和期望值比对的函数
       '''

    # 将返回结果解析成和用例中需要的一样的结果
    def parse_response_object(self, resp_obj):
        try:
            resp_body = resp_obj.json()
        except ValueError:
            resp_body = resp_obj.text
        return {
            'status_code': resp_obj.status_code,
            'headers': resp_obj.headers,
            'response': resp_body
        }

    # 对比接口返回的json和实际的是否一致
    def diff_json(self, current_json, expected_json):
        json_diff = {}
        for key, expected_value in expected_json.items():
            value = current_json.get(key, None)
            if str(value) != str(expected_value):
                json_diff[key] = {
                    'value': value,
                    'expected': expected_value
                }

        return json_diff

    # response.json响应结果和期望值的比较函数
    # 对比 status_code，将差异存入 diff_content
    # 对比 Headers，将差异存入 diff_content
    # 对比 Body，将差异存入 diff_content
    def diff_response(self, resp_obj, expected_resp_json):
        diff_content = {}
        resp_info = self.parse_response_object(resp_obj)
        if resp_info['status_code'] != expected_resp_json['status_code']:
            diff_content['status_code'] = {
                'value': resp_info['status_code'],
                'expected': expected_resp_json['status_code']
            }

        elif self.diff_json(resp_info['body'], expected_resp_json['response']):
            diff_content['body'] = {
                'value': resp_info['body'],
                'expected': expected_resp_json['response']
            }
        return diff_content

    # response.json响应结果和期望值的比较函数
    def asset_value(self, resp_obi, expected_json):
        print(resp_obi)
        if expected_json:
            for key, expect_value in expected_json.items():
                results = jsonpath.jsonpath(resp_obi.json(), key)
                if results:
                    assert results[0] == expect_value, '期望值为{},实际返回的值为{}'.format(expect_value, results)
                else:
                    assert False, '期望字段在响应结果中不存在'

    # 该函数用于用例在执行时实时更新用例
    def update_parameter(self, parameter):
        if Tools.output:
            list_params = json.dumps(parameter)
            for key, value in Tools.output.items():
                list_params = list_params.replace(f'${key}', str(value))
            list_params = json.loads(list_params)
        return list_params












if __name__ == '__main__':
    # dir = 'E://code/pytest/testcases/combinCase'
    # s = get_all_test_datas_extract(dir)
    # print(s)
    # file = 'E://code/pytest/testcases/combinCase/delete_api.yaml'
    # with open(file, encoding='utf-8') as f:
    #     dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
    # http = get_test_data('E://code/pytest/testcases/combinCase/login.yaml')
    # print(http)

    # s1 = [('使用正确的数据新增api密钥', {'method': 'POST', 'url': '/res/user/auth/api?X-CSRF-TOKEN=dvZL3veX', 'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Authorization': 'CB03BAA1E6C84DC2B352AC8706259F33', 'Content-Type': 'application/json;charset=UTF-8'}, 'json': {'remark': 'flychen', 'allow_ips': '', 'allow_trade': True, 'allow_withdraw': True, 'totp_captcha': {'validate_code': 111111, 'sequence': ''}}}, {'status_code': 200, 'response': {'data.allow_trade': True, 'data.allow_withdraw': True, 'code': 0}}, {'user_auth_id': 'data.user_auth_id'}), ('删除已存在的api密钥', {'method': 'DELETE', 'url': '/res/user/auth/api/$user_auth_id?X-CSRF-TOKEN=m0MQ3Wrt', 'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Authorization': 'CB03BAA1E6C84DC2B352AC8706259F33', 'Content-Type': 'application/json;charset=UTF-8'}, 'json': {'totp_captcha': {'validate_code': 111111, 'sequence': ''}}}, {'status_code': 200, 'response': {'code': 0}}, {})]
    #
    # print(s1[0][1].pop('method'))
    # print(s1)
    #
    s = {}
    if s:
        print('非空')
    else:
        print('空')
    try:
        print('hello')
    except KeyError:
        print('hello')









