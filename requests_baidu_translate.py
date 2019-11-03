#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 22:21
# @Author  : ZhangYang
# @File    : requests_baidu_translate.py

# 使用百度翻译URL实现中英互译
import json
import sys

import requests


class BaiduTranslate():
    def __init__(self, trans_str):
        self.trans_str = trans_str
        self.lang_detect_url = "https://fanyi.baidu.com/langdetect"
        self.lang_trans_url = "https://fanyi.baidu.com/v2transapi"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }
        pass
    def lang_detect(self):
        data ={"query":self.trans_str}
        # 获取输入字符串的语言类型
        responce = requests.post(self.lang_detect_url,headers=self.headers, data=data)
        lan = json.loads(responce.content.decode())["lan"]
        return lan

    def get_trans_data(self, lan=None):
        # 根据输入的语言类型， 判断中译英 还是 英译中
        trans_data = dict()
        trans_data["query"] = self.trans_str
        if lan == 'zh':
            trans_data["from"] = 'zh'
            trans_data["to"] = 'en'
        else:
            trans_data["from"] = 'en'
            trans_data["to"] = 'zh'
        return trans_data

    def lang_translate(self,trans_data=None):
        response = requests.post(self.lang_trans_url, headers=self.headers, data=trans_data)
        res_data = json.loads(response.content.decode())["trans_result"]["data"][0]["dst"]
        print("result is: {}".format(res_data))

    def run(self):
        # 获取输入的语言类型
        lan = self.lang_detect()
        # 判断中译英 还是 英译中
        trans_data = self.get_trans_data(lan)
        # 实现翻译转换
        self.lang_translate(trans_data=trans_data)

if __name__ == "__main__":
    trans_str = sys.argv[1]
    # trans_str = "你好"
    baidu_trans= BaiduTranslate(trans_str=trans_str)
    baidu_trans.run()

