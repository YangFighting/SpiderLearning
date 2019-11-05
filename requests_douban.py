#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 22:42
# @Author  : ZhangYang
# @File    : requests_douban.py

""" 使用 requests 请求豆瓣url, 该url返回的是json"""
import json

import requests


class DoubanSpider():
    def __init__(self):
        self.url_tv = "https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36"
        }

    def get_requests(self,get_url=None):
         # 请求url, 返回json字符串
        response = requests.get(get_url, headers=self.headers)
        html_json_str = response.content.decode()
        return html_json_str

    def get_content_list(self, json_str=None):
        # 解析json数据，获得内容序列
        dict_res = json.loads(json_str)
        content_list = dict_res["subjects"]
        return content_list

    def save_item(self, item=None):
        '''保存一个item'''
        with open(self.item_path_name, "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False, indent=2))
            f.write("\n")


    def run(self):
        num = 0
        # 1. 构造url
        url = self.url_tv.format(num)
        # 2. 请求url
        html_json_str = self.get_requests(get_url=url)
        # 3. 解析json数据
        item_list = self.get_content_list(json_str=html_json_str)
        # 4. 保存 item

        num +=20

if __name__ == "__main__":
    douban_spider = DoubanSpider()
    douban_spider.run()