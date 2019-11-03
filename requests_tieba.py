#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 16:56
# @Author  : ZhangYang
# @File    : requests_tieba.py

# 使用 requests 爬取贴吧，保存HTML
import os

import requests
class TiebaSpider:
    def __init__(self, tieba_name,max_page_num=10):
        self.tieba_name = tieba_name
        self.max_page_num = max_page_num
        self.folder_name = str(os.path.basename(__file__)).split('.',1)[0]

        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

        self.tieba_url = "http://tieba.baidu.com/f?ie=utf-8&kw={}".format(self.tieba_name)
        self.headers = {"User-Agent":
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}

    def get_url_list(self):
        "构造URL 列表"
        url_tup = list()
        for page_num_i in range(1, self.max_page_num+1):
            url_i = self.tieba_url + "&pn={}".format(page_num_i*50)
            url_tup.append(url_i)
        return url_tup

    def parse_requests(self, parse_url):
        "根据 url 获取requests"
        response = requests.get(parse_url,headers=self.headers)
        return response.content.decode()

    def save_html(self,html_str,page_num):
        "保存html"
        file_path = "./{0}/{1}_第{2}页.txt".format(self.folder_name, self.tieba_name, page_num)
        with open(file_path,"w",encoding="utf-8") as f:
            f.write(html_str)

    def run(self):
        # 构造URL 列表
        url_tup = self.get_url_list()
        for url_i in url_tup:
            # 发送请求，获取响应
            html_content=self.parse_requests(parse_url=url_i)
            # 保存
            self.save_html(html_str=html_content,page_num=url_tup.index(url_i)+1)

if __name__ == "__main__":
    tieba_spider = TiebaSpider(tieba_name='python', max_page_num=10)
    tieba_spider.run()