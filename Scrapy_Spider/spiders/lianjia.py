# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.http import Request
from Scrapy_Spider.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['gz.lianjia.com']
    start_urls = 'https://gz.lianjia.com/chengjiao/pg{page}/'

    custom_settings = {
        "COOKIES_ENABLED": False,
        "MONGODB_DBNAME": "LianJia",
        "DEFAULT_REQUEST_HEADERS": {
            "Host": "gz.lianjia.com",
        }
    }

    def start_requests(self):
        urls = [self.start_urls.format(page=page) for page in range(1, 101)]
        for url in urls:
            yield Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        """解析索引页"""
        detail_urls = response.xpath('//div[@class="info"]//div[@class="title"]//a//@href').extract()
        for url in detail_urls:
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        """解析详情"""
        lianjia_item = LianjiaItem()
        url = response.url
        id = re.search("(\d+)", response.url).group(1)
        title = response.xpath('//h1[@class="index_h1"]//text()').extract_first(default=None)
        deal_info = response.xpath('//div[@class="info fr"]')
        deal_price = deal_info.xpath('.//span[@class="dealTotalPrice"]//i//text()').extract_first()
        average_price = deal_info.xpath('.//b//text()').extract_first()
        base_info = response.xpath('//div[@class="base"]//li/text()').extract()
        base_info = [base.strip() for base in base_info]
        fileds = ["type", "floor", "covered_area", "structure_type", "inner_area", "building_type",
                  "orientation", "built_at", "decoration", "structure", "heating_mode", "one_floor",
                  "own_years", "is_elevator", "lianjia_code", "deal_type", "listing_dt", "house_usage",
                  "house_years", "house_belongs"]
        base_info = dict(zip(fileds, base_info))
        for filed, attr in base_info.items():
            lianjia_item[filed] = attr
        lianjia_item['url'] = url
        lianjia_item['id'] = id
        lianjia_item['title'] = title
        lianjia_item['deal_price'] = deal_price
        lianjia_item['average_price'] = average_price

        yield lianjia_item








