#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/30 23:30
# @Author  : ZhangYang
# @File    : requests_36kr.py

#在36kr首页上找到一个带有json的script，使用正则将json的提取出来
import json
from pprint import pprint

import requests
import re

kr_url = "https://36kr.com/"

response = requests.get(kr_url)
html_str = response.content.decode()
res_str_from_re = re.findall(r"<script>window.initialState=(.*)</script>", html_str)[0]

with open("36kr.json", "w", encoding="utf-8") as f:
    f.write(res_str_from_re)

res_json = json.loads(res_str_from_re)
pprint(res_json)

