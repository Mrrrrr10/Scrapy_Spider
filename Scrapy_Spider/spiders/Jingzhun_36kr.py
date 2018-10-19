# -*- coding: utf-8 -*-

import json
from scrapy.http import Request
from Scrapy_Spider.items import *

class Jingzhun36krSpider(scrapy.Spider):
    name = 'JingZhun_36kr'
    start_urls = ["https://rong.36kr.com/api/mobi-investor/company/column/{i}/list?funding=0&ts={ts}"]
    company_link = "https://rong.36kr.com/api/mobi-investor/v3/company/{ccid}"

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "36kr-Tou-iOS/3.0.1 (iPhone6S) (UID:-1); iOS 9.3.2; Scale/2.0",
            "Host": "rong.36kr.com",
        }
    }

    def start_requests(self):
        for i in range(3, 6):
            yield Request(url=self.start_urls[0].format(i=i, ts=0), meta={'i': i})

    def parse(self, response):
        data = response.text.get('data').get('data').get('cells')
        totalcount = response.text.get('data').get('data').get('totalCount')
        if data and not totalcount:
            i = response.meta.get('i')
            ts = response.text.get("data").get("ts")
            for one in data:
                if i == 3:
                    item = JingZhunLastedProjectItem()
                elif i == 4:
                    item = JingZhunLastedInvestmentItem()
                else:
                    item = JingZhunInFinancingItem()

                item['CompanyName'] = one.get("name")
                item['Logo'] = one.get("logo")
                item['CompanyCcid'] = one.get("ccid")
                item['CompanyRcid'] = one.get("rcid")
                item['FinancePhase'] = one.get("finance_phase")
                item['IndustryType'] = one.get("industry1")
                item['CompanyBrief'] = one.get("brief")
                item['IsExcellent'] = one.get("excellent")
                item['IsFunding'] = one.get("funding")
                item['HasBP'] = one.get("HasBP")
                item['PubDate'] = "20" + one.get("pubdate").replace('/', '-')

                yield Request(url=self.company_link.format(ccid=str(item['CompanyCcid'])), callback=self.parse_detail,
                              meta={'item': item})

            if not totalcount and ts:
                yield Request(url=self.start_urls[0].format(i=i, ts=ts), callback=self.parse, meta={'i': i})

    def parse_detail(self, response):
        item = response.meta.get("item")
        text_json = json.loads(response.text)
        data = text_json.get("data").get("pastFinance").get("data")
        item['CompanyFullName'] = text_json.get("data").get("projectInfo").get('fullName')
        item['RelatedLink'] = text_json.get("data").get("relatedLink").get('website')
        item['WeChat'] = text_json.get("data").get("relatedLink").get('weixin')
        member = text_json.get("data").get("member").get('data', None)
        item['Member'] = ",".join(["({0} {1})".format(item.get('investorId'), item['name']) for item in member]) if member else None
        item['Finance'] = text_json.get("data").get("basic").get('financeAmount', None)
        Address1Id = text_json.get("data").get("basic").get('address1Id')
        Address1 = text_json.get("data").get("basic").get('address1') if Address1Id else None
        Address2Id = text_json.get("data").get("basic").get('address2Id')
        Address2 = text_json.get("data").get("basic").get('address2') if Address2Id else None
        item['Address1'] = (Address1Id, Address1)
        item['Address2'] = (Address2Id, Address2)
        item['InvestEntity'] = ",".join(["{0} {1}".format(item.get('id'), item.get('name')) for item in data[0].get('investEntity', "")]) if data else None
        item['CompanyAsset'] = data[0].get('asset', "") if data else None
        tags = text_json.get("data").get('tags').get("data")
        item['IndustryTags'] = ' '.join([item.get("name", "") for item in tags]) if tags else None
        item['ProjectInfo'] = text_json.get("data").get("projectInfo").get('intro')

        yield item


