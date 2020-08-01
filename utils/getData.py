import yaml
import os, sys
sys.path.append(os.getcwd())
import json


# 获取单个yaml文件测试用例的接口
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

# 获取目录下的所以ymal文件
def get_all_files(dir):
    files_ = []
    file_path = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    for path in files_:
        file_path.append(path.replace('\\', '/'))
    return file_path


# 接口使用paramize函数调用的接口
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


# 获取confest传递参数的接口测试数据
def get_all_test_datas_extract(test_data_path):
    file_path = get_all_files(test_data_path)
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    extract = []  # 存储返回值
    for file in file_path:
        with open(file, encoding='utf-8') as f:
            dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
            test = dat['tests']
            for td in test:
                if td.get('run') == 'yes':  # run 为yes才执行，否则不用执行
                    case.append(td.get('case', ''))
                    http.append(td.get('request', {}))
                    expected.append(td.get('expected', {}))
                    extract.append(td.get('extract', {}))
    parameters = zip(case, http, expected, extract)
    parameters = list(parameters)
    return parameters

