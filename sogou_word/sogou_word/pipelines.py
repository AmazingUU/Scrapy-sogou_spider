# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline


class SogouWordPipeline(object):
    def process_item(self, item, spider):
        return item

class SogouWordFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'],meta={'filename':item['filename']})

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            print('下载失败')
            raise DropItem("Item contains no files")
        # item['file_paths'] = file_paths
        print('下载成功')
        return item

    def file_path(self, request, response=None, info=None):
        filename = request.meta['filename']
        path = os.path.join('D:\github\Scrapy-sogou_spider\sogou_word\sogou_word\download', filename + '.scel')
        return path