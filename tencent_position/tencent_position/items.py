# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentPositionItem(scrapy.Item):
    # define the fields for your item here like:
    position_name = scrapy.Field()  # 职位名称
    department = scrapy.Field()  # 工作部门
    base = scrapy.Field()  # 工作地点
    position_type = scrapy.Field()  # 职位类型
    publish_date = scrapy.Field()  # 发布时间
    responsibility = scrapy.Field()  # 工作职责
    requirement = scrapy.Field()  # 工作要求
    post_id = scrapy.Field()  # 工作岗位id 用于获取工作职责 和 工作要求
    position_url = scrapy.Field()  # 职位url
