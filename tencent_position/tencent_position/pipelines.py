# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json


class TencentPositionPipeline(object):
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def open_spider(self, spider):
        """ 在开启爬虫的时候执行， 只执行一次"""

        # 将文件清空
        with open(spider.settings.get("SAVE_FILE_NAME"), "w", encoding="utf-8") as f:
            f.write("")
        self.start_time = datetime.datetime.now()

    def close_spider(self, spider):
        self.end_time = datetime.datetime.now()
        print("程序运行时间：{}s".format((self.end_time - self.start_time).seconds))

    def process_item(self, item, spider):
        if item:
            with open(spider.settings.get("SAVE_FILE_NAME"), "a", encoding="utf-8") as f:
                json.dump(dict(item), f, ensure_ascii=False, indent=2)
        return item
