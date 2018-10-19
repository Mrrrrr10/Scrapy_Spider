# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import pymongo
import MySQLdb
import MySQLdb.cursors
from Scrapy_Spider.items import *
from openpyxl import Workbook
from twisted.enterprise import adbapi       # adbapi可以将Mysql的操作变为异步化的操作

class ScrapySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

# ---------- MongoDB_Pipeline ----------
class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_HOST'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DBNAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.__class__.__name__].create_index([('id', pymongo.ASCENDING)])
        self.db[item.__class__.__name__].update({'id': item.get('id')}, {'$set': item}, True)

        return item


# ---------- MySQL_Pipeline ----------
class MysqlTwistedPipeline(object):
    """
    处理所有的MySQL插入
    Twisted提供异步操作,异步容器 连接池
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """dict()里面的参数名称也是固定的,与MySQL模块的connections提供的参数名要一致"""
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)   # adbapi可以将Mysql的操作变为异步化的操作
        return cls(dbpool)

    def process_item(self, item, spider):
        """使用twisted将MySQL插入变成异步执行"""
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.address_error, item, spider)      # 处理异常

    def address_error(self, failure, item, spider):
        """错误处理"""
        print(failure)

    def do_insert(self, cursor, item):
        """
        执行具体的插入,
        根据不同的item构建不同的sql语句并插入到mysql中
        """
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

# ---------- Excel_Pipeline ----------
class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws_product = self.wb.active
        self.ws_comment = self.wb.active
        self.filed_list = []
        self.line_list = []

    def process_item(self, item, spider):
        """工序具体内容"""
        for filed in item.fileds:
            self.filed_list.append(filed)
            self.line_list.append(item[filed])
        self.ws_product.append(self.filed_list)                 # 设置表头
        self.ws_product.append(self.line_list)                  # 将数据以行的形式添加到xlsx中
        self.wb.save('E:/%s.xlsx' % item.__class__.__name__)    # 保存xlsx文件
        return item

# ---------- Time_Pipeline ----------
class TimePipeline():
    def process_item(self, item, spider):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['crawled_at'] = now

        return item

# ---------- Amazon_Pipeline ----------
class Amazon_Pipeline():
    def process_item(self, item, spider):
        if isinstance(item, AmazonItem) or isinstance(item, AmazonCommentItem):
            if item.get('title'):
                item['title'] = item['title'].strip()
            if item.get('desc'):
                item['desc'] = item['desc'].strip()
            if item.get('size'):
                item['size'] = item['size'].strip()
            if item.get('weight'):
                item['weight'] = item['weight'].strip()

            if item.get('text'):
                item['text'] = item['text'].strip()

            if item.get('date'):
                item['date'] = item['date'].replace('于 ', '-').replace('年', '-').replace('月', '-').replace('日', '')

        return item

