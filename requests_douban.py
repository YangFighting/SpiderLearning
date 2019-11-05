#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 22:42
# @Author  : ZhangYang
# @File    : requests_douban.py

"""
    使用 requests 请求豆瓣热门电视剧url, 该url返回的是json
    找到该url的方式是：点击 热门电视剧 下面的首页

"""
import json
import os

import requests


class DoubanSpider():
    def __init__(self):
        self.page_limit = 20
        self.url_tv = "https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit="+ str(self.page_limit) + "&page_start={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36"
        }
        self.item_file_name = u'豆瓣电视剧.txt'
        self.item_folder_name = 'douban_files'
        self.item_path_name = os.path.join(os.getcwd(), self.item_folder_name, self.item_file_name)

        if not os.path.exists(self.item_folder_name):
            os.mkdir(self.item_folder_name)
        # 初始化txt
        with open(self.item_path_name, "w") as f:
            f.write("")

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

    def save_item(self, item_list=None):
        '''保存一个item'''
        with open(self.item_path_name, "a", encoding="utf-8") as f:
            for item_i in item_list:
                f.write(json.dumps(item_i, ensure_ascii=False, indent=2))
                f.write("\n")


    def run(self):
        num = 0
        while True:
            # 1. 构造url
            url = self.url_tv.format(num)
            # 2. 请求url
            html_json_str = self.get_requests(get_url=url)
            # 3. 解析json数据
            item_list = self.get_content_list(json_str=html_json_str)
            # 4. 保存 item
            self.save_item(item_list=item_list)
            if  len(item_list) < self.page_limit:
                print("总计：{}部电视剧".format(num + len(item_list)))
                break
            num += 20

if __name__ == "__main__":
    douban_spider = DoubanSpider()
    douban_spider.run()