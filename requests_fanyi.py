#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 16:53
# @Author  : ZhangYang
# @File    : requests_fanyi.py

"使用 request 发送 Post请求 ，实现翻译"

import json
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}
post_url = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"

def query_data(input_data = None):
    data = {
        "from": "zh",
        "to": "en",
        "query": str(input_data),
        "transtype": "translang"
    }
    return data

res = requests.post(post_url,headers=headers, data=query_data(input_data="你好"))
res_dict = json.loads(res.content.decode())
if res_dict['errno'] == 0:
    res_data = res_dict["trans_result"]["data"][0]["dst"]
    print(res_data)
else:
    print("errno: {0}".format(res_dict['errno']))
    print("翻译出错")