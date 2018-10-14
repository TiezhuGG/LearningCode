# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo
from twisted.enterprise import adbapi
from jianshu import settings


# mongodb存储
class MongoPipeline(object):

    collection_name = 'article'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        print('正在存入mongodb:', dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


# mysql异步存储
class MysqlTwistedPipeline(object):
    def __init__(self, host, database, user, password, port):
        dbparams = dict(
            host = host,
            database = database,
            user = user,
            password = password,
            port = port,
            cursorclass = pymysql.cursors.DictCursor
        )
        # 使用twisted库中的adbapi获取数据库连接池对象
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def process_item(self, item, spider):
        # 使用twisted将mysql插入操作变成异步执行，采用异步的机制写入mysql
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)

    def do_insert(self,cursor,item):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        # mysql插入语句:_sql
        _sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        cursor.execute(_sql, tuple(data.values()))
        print('正在插入数据:',dict(item))
        return item

    def handle_error(self, error, spider):
        # 处理异步插入的异常
        spider.logger.error(error)

