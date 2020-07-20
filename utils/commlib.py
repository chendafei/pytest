import yaml
import json
import jsonpath
import os
class CommUtil(object):

    def get_test_data(self, test_data_path):
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

if __name__ == '__main__':
    dir = 'E://code/pytest/testcases'
    l = get_all_files(dir)
    print(l)
