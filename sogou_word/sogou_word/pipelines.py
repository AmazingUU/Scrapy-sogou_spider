# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.pipelines.files import FilesPipeline


class SogouWordPipeline(object):
    def process_item(self, item, spider):
        return item

class SogouWordFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'],meta={'filename':item['filename']})

    def file_path(self, request, response=None, info=None):
        filename = request.meta['filename']
        path = os.path.join('D:\github\Scrapy-sogou_spider\sogou_word\sogou_word\download', filename + '.scel')
        return path