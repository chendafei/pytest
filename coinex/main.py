#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Created on 2020年1月13日15:58:33


使用说明：
1.替换test_coinex_api_auto.py中的密钥，用于测试
2.准备一个长久有效的秘钥放在api_zhushou.py，用于造数
3.设置提现白名单
4.需要充足的ETH、LTC、BTC、USDT
5.检查币币市场LTCUSDT是否可用
6.检查期货市场BTCFCNY是否可用，不可用替换相关案例
7.修改输出报告的名字，运行
"""

from __future__ import unicode_literals
import os
import time
import unittest
import hashlib
import json as complex_json
import urllib3
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1, read=2))
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('mylog')
BASEDIR = os.path.dirname(os.path.abspath(__file__))

class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, headers={}):
        #这里放测试用的秘钥
        self.access_id = '424BBB7A8A194E7FA308CD15AE5D99EB'      # replace
        self.secret_key = '728DD14A28904987831D78BFB948AA7F0CD9BCA81F42878D'     # replace
        self.url = 'http://testapi3.coinex.com'
        self.headers = self.__headers
        self.headers.update(headers)

    @staticmethod
    def get_sign(params, secret_key):
        sort_params = sorted(params)
        data = []
        for item in sort_params:
            data.append(item + '=' + str(params[item]))
        str_params = "{0}&secret_key={1}".format('&'.join(data), secret_key)
        #logger.info(str_params)
        token = hashlib.md5(str_params.encode()).hexdigest().upper()
        #logger.info(token)
        return token

    def set_authorization(self, params):
        params['access_id'] = self.access_id
        params['tonce'] = int(time.time()*1000)
        self.headers['AUTHORIZATION'] = self.get_sign(params, self.secret_key)

    def request(self, method, url, params={}, data='', json={}):
        '''
        @params: GET 和 DELETE 调用时参数使用
        @json： 其他参数传入这个
        '''
        method = method.upper()
        if method in ['GET', 'DELETE']:
            self.set_authorization(params)
            result = requests.request(method, url, fields=params, headers=self.headers)
        else:
            if data:
                json.update(complex_json.loads(data))
            self.set_authorization(json)
            encoded_data = complex_json.dumps(json).encode('utf-8')
            result = http.request(method, url, body=encoded_data, headers=self.headers)
        return result

# 下普通订单
def test_orderlimit():
    request_client = RequestClient()
    data = {
        "account_id": 0,
        "amount": "1",
        "price": "9000",
        "type": "sell",
        "market": "BTCUSDT"
    }
    response = request_client.request(
        'POST',
        '{url}/v1/order/limit'.format(url=request_client.url),
        json=data,
    )
    result = complex_json.loads(response.data)
    print(complex_json.loads(response.data))
    assert response.status == 200
    assert result['message'] == 'Ok'

# 下杠杠单
def test_ordermaginlimit():
    request_client = RequestClient()
    data = {
        "account_id": 2,
        "amount": "1",
        "price": "9000",
        "type": "sell",
        "market": "BTCUSDT"
    }
    response = request_client.request(
        'POST',
        '{url}/v1/order/limit'.format(url=request_client.url),
        json=data,
    )
    result = complex_json.loads(response.data)
    print(complex_json.loads(response.data))
    assert response.status == 200
    assert result['message'] == 'Ok'

# 下合约单
# 站内转账
def test_localwithdraw():
    request_client = RequestClient()
    data = {
        "actual_amount": "100",
        "coin_address": "1657214485@qq.com",
        "coin_type": "cet",
        "smart_contract_name": "CoinExChain",
        "transfer_method": "local"
    }
    response = request_client.request(
        'POST',
        '{url}/v1/balance/coin/withdraw'.format(url=request_client.url),
        json=data
    )
    result = complex_json.loads(response.data)
    print(complex_json.loads(response.data))
    assert response.status == 200
    assert result['message'] == 'Ok'

# 站外转账
def test_onchainwithdraw():
    request_client = RequestClient()
    data = {
        "actual_amount": "0.01",
        "coin_address": "0x4d5992030e6f9376ec441cdc82a6ef5cdc3d804a",
        "coin_type": "eth",
        "smart_contract_name": "ERC20",
        "transfer_method": "onchain"
    }
    response = request_client.request(
        'POST',
        '{url}/v1/balance/coin/withdraw'.format(url=request_client.url),
        json=data
    )
    result = complex_json.loads(response.data)
    print(complex_json.loads(response.data))
    assert response.status == 200
    assert result['message'] == 'Ok'

#
# if __name__ =="__main__":
