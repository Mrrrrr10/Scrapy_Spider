# -*- coding: utf-8 -*-

import re
import scrapy
from urllib import parse
from scrapy.http import Request
from Scrapy_Spider.items import TripadvisorItem


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/TravelersChoice-Destinations-cTop-g1']
    hotel_page_url = "https://www.tripadvisor.com/Hotels-{0}-oa{1}-{2}-Hotels.html"

    def parse(self, response):
        target_url = [parse.urljoin(response.url, url) for url in
                      response.xpath('//div[@class="mainName"]//a//@href').extract()]
        for url in target_url:
            yield Request(url=url, callback=self.parse_destination_url)

    def parse_destination_url(self, response):
        """解析Top25景点，从中提取酒店索引页url"""
        hotels_twoLines = response.xpath('//li[@class="hotels twoLines"]')
        winners = response.xpath('//div[@class="winners"]')
        if hotels_twoLines:
            hotel_page_url = parse.urljoin(response.url, hotels_twoLines.xpath('a/@href').extract_first())
            yield Request(url=hotel_page_url, callback=self.get_hotel_page)
        elif winners:
            hotel_url = parse.urljoin(response.url, winners.xpath('div[1]/ul/li/a/@href').extract_first())
            yield Request(url=hotel_url, callback=self.parse_hotel_detail)

    def get_hotel_page(self, response):
        """获取每个景点的酒店的所有列表页"""
        page_num = response.xpath('//div[@class="pageNumbers"]/a[last()]/@data-page-number').extract_first()
        offset = [item * 30 for item in range(1, int(page_num))]
        code = re.search('https.*Hotels-(.*?)-(.*?)-.*html', response.url).group(1)
        name = re.search('https.*Hotels-(.*?)-(.*?)-.*html', response.url).group(2)
        hotel_page_url = [self.hotel_page_url.format(code, num, name) for num in offset]
        hotel_page_url.insert(0, response.url)  # 列表页url
        for url in hotel_page_url:
            yield Request(url=url, callback=self.parse_hotel_page)

    def parse_hotel_page(self, response):
        """解析酒店列表页，提取出酒店url"""
        hotel_bashurl = response.xpath('//div[@class="listing_title"]/a/@href').extract()
        hotel_urls = [parse.urljoin(response.url, url) for url in hotel_bashurl]
        for url in hotel_urls:
            yield Request(url=url, callback=self.parse_hotel_detail)

    def parse_hotel_detail(self, response):
        """解析酒店详情"""
        item = TripadvisorItem()
        item['hotel_url'] = response.url
        item['hotel_en_name'] = response.xpath('//h1[@id="HEADING"]/text()').extract_first()
        if response.xpath('//span[@data-sizegroup="viewdealtext"]'):
            website = response.xpath('//img[@class="providerImg"]/@alt').extract()
            price = response.xpath('//div[@data-sizegroup="hr_chevron_prices"]/@alt').extract()
        else:
            website = response.xpath('//div[@class="ui_column providerLogo"]/img/@alt').extract()
            price = response.xpath('//div[@class="bb_price_text "]/text()').extract()
        item['hotel_price'] = list(zip(website, price)) if len(website) > 0 and len(price) > 0 else None
        hotel_score = response.xpath('//div[@class="ratingContainer"]/a/div/span/@alt').extract_first()
        item['hotel_score'] = hotel_score.replace(' of 5 bubbles', None) if hotel_score else None
        comments = response.xpath('//span[@class="reviewCount"]/text()').extract_first()
        item['comments'] = re.search('(\d+)', comments).group(1) if comments else None
        item['hotel_rating'] = response.xpath(
            '//span[@class="header_popularity popIndexValidation"]/b/text()').extract_first()
        item['hotel_addr'] = ' '.join(
            response.xpath('//div[@class="is-hidden-mobile blEntry address ui_link "]/span[2]/span/text()').extract())
        item['hotel_location'] = '-'.join(
            response.xpath('//div[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li/a/span/text()').extract())
        item['userlocation'] = []
        yield Request(url=response.url, callback=self.parse_user, meta={'item': item}, dont_filter=True)

    def parse_user(self, response):
        """解析用户位置"""
        item = response.meta.get('item')
        userlocation = response.xpath('//div[@class="userLoc"]/strong/text()').extract()
        item['userlocation'].extend(userlocation)
        next = response.xpath('//a[@class="nav next taLnk ui_button primary"]')
        if next:
            next_url = parse.urljoin(response.url, next.xpath('@href').extract_first())
            yield Request(url=next_url, callback=self.parse_user, meta={'item': item})
        else:
            print('hotel_en_name:%s\nhotel_ratevalue:%s\nhotel_rating:%s\nhotel_addr:%s\nhotel_location:%s\n'
                  'hotel_price:%s\nuserlocation:%s'
                  % (item['hotel_en_name'], item['hotel_score'], item['hotel_rating'],
                     item['hotel_addr'], item['hotel_location'], item['hotel_price'],
                     item['userlocation']))
            yield item
