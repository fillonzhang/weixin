# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from twisted.enterprise import adbapi
from scrapy.http import Request


class WeixinPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    #项目管理通道，用来处理spider抓取的数据
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.haddle_error)

    def haddle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        sql = """insert into weixin_img(title_name, category, metadataFileSize, metadataFileFormat,
        md5val, imageFinishTime, source_url, basic_url, imageClarity, CC0, Medium
        ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql,
                       (item["title_name"], item["category"], item["metadataFileSize"],
                        item["metadataFileFormat"], item["md5val"], item["imageFinishTime"], item["source_url"],
                        item["basic_url"], item["imageClarity"], item["CC0"], item["Medium"]
                        ))
        print("save mysql", item)


