import yaml
import json
import jsonpath
import os


def get_test_data(test_data_path):
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    with open(test_data_path, encoding='utf-8') as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test = dat['tests']
        for td in test:
            case.append(td.get('case', ''))
            http.append(td.get('request', {}))
            expected.append(td.get('expected', {}))
    parameters = zip(case, http, expected)
    return case, parameters


# 将返回结果解析成和用例中需要的一样的结果
def parse_response_object(resp_obj):
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
def diff_json(current_json, expected_json):
    json_diff = {}
    for key, expected_value in expected_json.items():
        value = current_json.get(key, None)
        if str(value) != str(expected_value):
            json_diff[key] = {
                'value': value,
                'expected': expected_value
            }

    return json_diff


def diff_response(resp_obj, expected_resp_json):
    diff_content = {}
    resp_info = parse_response_object(resp_obj)
    if resp_info['status_code'] != expected_resp_json['status_code']:
        diff_content['status_code'] = {
            'value': resp_info['status_code'],
            'expected': expected_resp_json['status_code']
        }

    elif diff_json(resp_info['body'], expected_resp_json['response']):
        diff_content['body'] = {
            'value': resp_info['body'],
            'expected': expected_resp_json['response']
        }
    return diff_content
    # 对比 status_code，将差异存入 diff_content
    # 对比 Headers，将差异存入 diff_content
    # 对比 Body，将差异存入 diff_content


def asset_value(resp_obi, expected_json):
    print(resp_obi)
    results = []
    if expected_json:
        for key, expect_value in expected_json.items():
                results = jsonpath.jsonpath(resp_obi.json(), key)
                if results:
                    assert results[0] == expect_value, '期望值为{},实际返回的值为{}'.format(expect_value, results)
                else:
                    assert False, '期望字段在响应结果中不存在'

def get_all_files(dir):
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    for i in list_:
        i.replace('\\', '/')
    return files_

def get_all_test_datas(test_data_path):
    file_path = get_all_files(test_data_path)
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    for file in file_path:
        with open(file, encoding='utf-8') as f:
            dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
            test = dat['tests']
            for td in test:
                case.append(td.get('case', ''))
                http.append(td.get('request', {}))
                expected.append(td.get('expected', {}))
    parameters = zip(case, http, expected)
    return case, parameters

def get_all_test_datas_extract(test_data_path):
    # file_path = get_all_files(test_data_path)
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    extract = []  # 存储返回值
    with open(test_data_path, encoding='utf-8') as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test = dat['tests']
        print(test)
        for td in test:
            case.append(td.get('case', ''))
            http.append(td.get('request', {}))
            expected.append(td.get('expected', {}))
            extract.append(td.get('extract', {}))
    parameters = zip(case, http, expected, extract)
    parameters = list(parameters)
    return parameters


if __name__ == '__main__':
    dir = 'E://code/pytest/testcases/API-Manager/delete_api.yaml'
    s = get_all_test_datas_extract(dir)
    print(s)
    s1 = [('使用正确的数据新增api密钥', {'method': 'POST', 'url': '/res/user/auth/api?X-CSRF-TOKEN=dvZL3veX', 'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Authorization': 'CB03BAA1E6C84DC2B352AC8706259F33', 'Content-Type': 'application/json;charset=UTF-8'}, 'json': {'remark': 'flychen', 'allow_ips': '', 'allow_trade': True, 'allow_withdraw': True, 'totp_captcha': {'validate_code': 111111, 'sequence': ''}}}, {'status_code': 200, 'response': {'data.allow_trade': True, 'data.allow_withdraw': True, 'code': 0}}, {'user_auth_id': 'data.user_auth_id'}), ('删除已存在的api密钥', {'method': 'DELETE', 'url': '/res/user/auth/api/$user_auth_id?X-CSRF-TOKEN=m0MQ3Wrt', 'headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Authorization': 'CB03BAA1E6C84DC2B352AC8706259F33', 'Content-Type': 'application/json;charset=UTF-8'}, 'json': {'totp_captcha': {'validate_code': 111111, 'sequence': ''}}}, {'status_code': 200, 'response': {'code': 0}}, {})]

    print(s1[0][1].pop('method'))
    print(s1)

    s = {}
    if s:
        print('非空')
    else:
        print('空')


