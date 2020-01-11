# -*- coding: utf-8 -*-
#定义需要获取的内容字段，类似实体类
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item  import Item,Field


class WeixinItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    year = Field()
    score = Field()
    director = Field()
    classification = Field()
    actor = Field()
    pass
