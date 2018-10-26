# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SogouWordItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()  # 词库下载url
    filename = scrapy.Field()  # 文件名
    cate1 = scrapy.Field()  # 一级分类
    cate2 = scrapy.Field()  # 二级分类
