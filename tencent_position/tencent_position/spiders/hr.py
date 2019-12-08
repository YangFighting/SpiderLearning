# -*- coding: utf-8 -*-
import json

import scrapy
import logging
from tencent_position.items import TencentPositionItem
logger = logging.getLogger(__name__)


class HrSpider(scrapy.Spider):

    def __init__(self):
        self.pageIndex = 1
        self.max_page_Index = 2
        self.pageSize = 10
        super().__init__()

    name = 'hr'
    allowed_domains = ['tencent.com']

    start_urls = [
        'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize={}'.format(1, 10)]

    def parse(self, response):
        title_list = json.loads(response.text)["Data"]["Posts"]
        if not title_list:
            logger.warning(
                'title is none https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize={}'
                    .format(self.pageIndex, self.pageSize))
            return None

        for title_i in title_list:
            position_item = TencentPositionItem()
            position_item["position_name"] = title_i.get("BGName")
            position_item["department"] = title_i.get("RecruitPostName")
            if title_i.get("CountryName") and title_i.get("LocationName"):
                position_item["base"] = title_i.get("CountryName") + "/" + title_i.get("LocationName")
            elif (not title_i.get("CountryName")) and title_i.get("LocationName"):
                position_item["base"] = title_i.get("LocationName")
            elif title_i.get("CountryName") and (not title_i.get("LocationName")):
                position_item["base"] = title_i.get("CountryName")
            else:
                position_item["base"] = ""
            position_item["position_type"] = title_i.get("CategoryName")
            position_item["publish_date"] = title_i.get("LastUpdateTime")
            position_item["post_id"] = title_i.get("PostId")

            # 获取详情
            post_id_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?&postId={}&language=zh-cn". \
                format(position_item["post_id"])
            yield scrapy.Request(post_id_url, callback=HrSpider.parse_detail, meta={"item": position_item})

            # 翻页请求
            if len(title_list) == self.pageSize and self.pageSize <= self.max_page_Index:
                self.pageIndex += 1
                next_page_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize={}' \
                    .format(self.pageIndex, self.pageSize)
                yield scrapy.Request(next_page_url, callback=self.parse)

    @staticmethod
    def parse_detail(response):
        position_item = response.meta.get("item")
        detail_dict = json.loads(response.text)["Data"]
        if not detail_dict:
            return None
        position_item["requirement"] = detail_dict.get("Requirement")
        position_item["responsibility"] = detail_dict.get("Responsibility")
        position_item["position_url"]  =detail_dict.get("PostURL")

        yield position_item
