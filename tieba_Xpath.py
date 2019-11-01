# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 17:05
# @Author  : ZhangYang
# @File    : tieba_Xpath.py
import os

import requests
from lxml import etree
import json


class Tieba:
    """
    使用lxml中的xpath 爬取贴吧中的图片
        UA用的是手机端，电脑端的UA，爬取的标签会隐藏
    """
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name  # 接收贴吧名
        # 电脑端的UA
        # self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}

        # 手机端的UA
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36"}
        self.item_file_name = u'贴吧图片.txt'
        self.item_folder_name = 'tieba_files'
        self.item_path_name = os.path.join(os.getcwd(), self.item_folder_name, self.item_file_name)

        if not os.path.exists(self.item_folder_name):
            os.mkdir(self.item_folder_name)

    def get_total_url_list(self):
        '''获取所有的urllist'''
        url = "https://tieba.baidu.com/f?kw=" + self.tieba_name + "&ie=utf-8&pn={}"
        url_list = []
        for i in range(0, 5):  # 通过循环拼接100个url
            url_list.append(url.format(i * 30))
        return url_list  # 返回100个url的urllist

    def parse_url(self, url=None):
        '''一个发送请求，获取响应，同时etree处理html'''
        print("parsing url:", url)
        response = requests.get(url, headers=self.headers, timeout=10)  # 发送请求
        html = response.content.decode()  # 获取html字符串
        html_etree = etree.HTML(html)  # 获取element 类型的html
        return html_etree

    def get_title_href(self, url=None):
        '''获取一个页面的title和href'''
        html_etree = self.parse_url(url)

        li_list = html_etree.xpath("//li[@class='tl_shadow tl_shadow_new ']")  # 手机端的li 标签
        total_items = []
        for li_i in li_list:  # 遍历分组
            href_list = li_i.xpath("./a/@href")
            # 每个帖子的链接
            href = "http://tieba.baidu.com" + href_list[0] if len(href_list) > 0 else None
            # 每个帖子的主题
            title_list = li_i.xpath("./a/div[1]/span[1]/text()")
            title = title_list[0] if len(title_list) > 0 else None
            item = dict(  # 放入字典
                href=href,
                title=title
            )

            total_items.append(item)
        return total_items  # 返回一个页面所有的item

    def get_img(self, url=None):
        '''获取一个帖子里面的所有图片'''
        html_etree = self.parse_url(url)
        # 提取图片的url，有的图片在主题里，有的在评论里
        img_list = html_etree.xpath('//div[@class="pb_img_item"]/@data-url|//div[@class="BDE_Image"]/@data-url')
        img_list = [i.split("src=")[-1] for i in img_list]
        # url解码
        img_list = [requests.utils.unquote(i) for i in img_list]
        return img_list

    def save_item(self, item=None):
        '''保存一个item'''
        with open(self.item_path_name, "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False, indent=2))
            f.write("\n")

    def run(self):
        # 1、找到了url规律，url list
        url_list = self.get_total_url_list()

        for url in url_list:
            # 2、遍历urllist 发送请求，获得响应，etree处理html
            # 3、提取title，href
            total_item = self.get_title_href(url)
            for item in total_item:
                href = item["href"]
                img_list = self.get_img(href)  # 获取到了帖子的图片列表
                item["img"] = img_list
                # 4、保存到本地
                print(item)
                self.save_item(item)


if __name__ == "__main__":
    tieba = Tieba("猫")
    tieba.run()
