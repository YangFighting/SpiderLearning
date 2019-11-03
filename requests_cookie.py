#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 16:55
# @Author  : ZhangYang
# @File    : requests_cookie.py

"CookieJar对象 与 dict之间的转换"
import requests

response = requests.get("http://www.baidu.com/")
#  返回CookieJar对象:
cookiejar = response.cookies
#  将CookieJar转为字典：
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
print (cookiejar)
print (cookiedict)