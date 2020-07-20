import pytest
import requests

# 使用正确的值新增api密钥

def test_add_api():
    url = 'http://test3.coinex.com/res/user/auth/api?X-CSRF-TOKEN=dvZL3veX'
    header = {
        "Content-Type": "application/json",
        "Authorization": "1A8B4D49C99740DD9FB968EFD220ECF3",
        "Accept-Language": "zh_Hans_CN"
    }
    data = {
        "remark": "陈飞",
        "allow_ips": "",
        "allow_trade": True,
        "allow_withdraw": False,
        "totp_captcha":
    {
        "validate_code": "111111",
        "sequence": ""
    }
    }
    re = requests.post(url, headers=header, json=data)
    print(re.json())
    assert re.json()['code'] == 0
    assert re.json()['data']['allow_trade'] == True

def test_delete_api():
    test_add_api()


if __name__ == '__main__':
    current_json = {"response":{"allow":True}}
    expected_json = {"response":{'code':0,'allow':True}}
    json_diff = {}
    for key, expect_value in expected_json.items():
        json_diff[key] = current_json.get(key)
    print(json_diff)


