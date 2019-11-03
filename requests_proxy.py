#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 16:52
# @Author  : ZhangYang
# @File    : requests_proxy.py

"使用代理发送requests请求"
import requests

# 免费代理网站：https://proxy.mimvp.com/free.php
# 检测IP是否可用
#   1. 判断访问时间
#   2. 在线检测
proxies = {
    "http": "http://117.28.245.75:80",
    "https": "http://182.61.20.200:808",
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}

responce = requests.get("http://www.baidu.com",headers=headers,proxies=proxies)
print(responce.status_code)