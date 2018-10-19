# -*- coding: utf-8 -*-

import re
import scrapy
from urllib import parse
from scrapy.http import Request
from Scrapy_Spider.items import AmazonItem, AmazonCommentItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/global-store/ranking/bestseller/']

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "RETRY_TIMES": 10,
        "COOKIES_ENABLED": False,
        "MONGODB_DBNAME": "Amazon",
        'ITEM_PIPELINES': {
            'Scrapy_Spider.pipelines.TimePipeline': 300,
            'Scrapy_Spider.pipelines.Amazon_Pipeline': 301,
            'Scrapy_Spider.pipelines.MongoPipeline': 302,
        },
    }

    def parse(self, response):
        # 解析每一个项目的url
        urls = response.xpath('//li[@class="rank_browser_item"]//a/@href').extract()
        urls = [url.replace('http', 'https') for url in urls]
        for url in urls:
            yield Request(url=url, callback=self.parse_index)

        yield Request(url="https://www.amazon.cn/gp/global-store/ranking/bestseller/baby/462-8766399-2378754",
                      callback=self.parse_index)

    def parse_index(self, response):
        # 解析索引页每个商品的url
        urls = response.xpath('//div[@class="a-section a-spacing-mini a-carousel-photo"]/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="a-text-center"]/ul/li[last()]/a/@href').extract_first()
        if next_page:
            next_page = next_page.replace('http', 'https')
            yield Request(url=next_page, callback=self.parse_index)

    def parse_detail(self, response):
        # 解析商品详情
        amazon_item = AmazonItem()
        id = re.search('dp\/(.*?)\/', response.url).group(1)
        amazon_item['id'] = id
        amazon_item['url'] = response.url
        amazon_item['title'] = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        amazon_item['price'] = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
        amazon_item['is_popular'] = response.xpath('//div[@class="badge-wrapper "]/i/text()').extract_first()
        amazon_item['brand'] = response.xpath('//a[@id="bylineInfo"]/text()').extract_first()
        amazon_item['desc'] = response.xpath('//div[@id="productDescription"]/p/text()').extract_first()
        amazon_item['size'] = response.xpath('//li[contains(b, "商品尺寸:")]/text()').extract_first()
        amazon_item['weight'] = response.xpath('//li[contains(b, "商品重量: ")]/text()').extract_first()
        amazon_item['score'] = response.xpath('//li[contains(b, "用户评分:")]//span[@class="a-icon-alt"]//text()').re_first('([0-9]\.[0-9])')
        comments_count = response.xpath('//li[contains(b, "用户评分:")]//span[@class="a-size-small"]//text()')
        amazon_item['comments_count'] = comments_count.re_first('(\d+)') if comments_count else None

        yield amazon_item
        
        comment_1st_url = response.xpath('//*[@id="acrCustomerReviewLink"]/@href').extract_first()
        if comment_1st_url:
            yield Request(url=parse.urljoin(response.url, comment_1st_url), callback=self.parse_comment, meta={'good_id': id, 'crawled_times': 0})

    def parse_comment(self, response):
        crawled_times = response.meta.get('crawled_times')
        self.logger.debug('Crawled times:%s\n%s' % (crawled_times, response.url))
        good_id = response.meta.get('good_id')
        comments = response.xpath('//div[@id="cm_cr-review_list"]')
        if comments:
            comment_item = AmazonCommentItem()
            for comment in comments:
                id = comment.xpath('.//div/@id').extract_first()
                score = comment.xpath('.//span[@class="a-icon-alt"]//text()').re_first('([0-9]\.[0-9])')
                title = comment.xpath('.//a[@data-hook="review-title"]//text()').extract_first()
                user = comment.xpath('.//a[@data-hook="review-author"]//text()').extract_first()
                date = comment.xpath('.//span[@data-hook="review-date"]//text()').extract_first()
                text = comment.xpath('.//span[@data-hook="review-body"]//text()').extract_first()
                user_url = parse.urljoin(response.url, comment.xpath('.//a[@data-hook="review-author"]/@href').extract_first())
                print(id, score, title, user, date, text, user_url)
                for filed in comment_item.fields:
                    try:
                        comment_item[filed] = eval(filed)  # 动态赋值,但是如果filed未定义,会抛出异常
                    except NameError:
                        self.logger.debug("filed is not defined：" + filed)

                comment_item['good_id'] = good_id

                yield comment_item

        self.logger.debug("Deciding whether to exist the next page")
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            crawled_times += 1
            next_page = parse.urljoin(response.url, next_page)
            self.logger.debug('Exist the next page:%s\nKeep crawling the next page' % next_page)
            yield Request(url=next_page, callback=self.parse_comment, meta={'crawled_times': crawled_times, 'good_id': good_id})
        else:
            self.logger.debug('Inexistence \nCrawling over!')

