# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline


class SogouWordPipeline(object):  # 将数据存入数据库
    db = pymysql.connect('***', '***', '***', '***', charset='utf8')

    def insert(self, item):
        sql = 'insert into detail(url,filename,cate1,cate2,create_time) values(%s,%s,%s,%s,now())'
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql, (item['url'], item['filename'], item['cate1'], item['cate2']))
                self.db.commit()
        except Exception as e:
            print('insert fail,e:', str(e))

    def process_item(self, item, spider):
        self.insert(item)
        return item


class SogouWordFilePipeline(FilesPipeline):  # 下载文件
    def get_media_requests(self, item, info):
        # 该方法不重写的话为：
        # for file_url in item['file_urls']:
        #     yield scrapy.Request(file_url)
        # 即如果item中定义了file_urls字段，且有使用FilesPipeline的类，该字段自动进入FilesPipeline中处理
        # 但是要求item['file_urls']为列表，我这里的下载url不是列表而且需要处理文件名问题，所以就重写了一下
        yield scrapy.Request(item['url'], meta={'filename': item['filename']})

    def item_completed(self, results, item, info):  # 下载完成时调用
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            print('下载失败')
            raise DropItem("Item contains no files")
        # item['file_paths'] = file_paths
        print('下载成功')
        return item

    def file_path(self, request, response=None, info=None):  # 文件名
        filename = request.meta['filename']  # 这里request的meta来自get_media_requests()
        basedir = os.getcwd()
        download_dir = os.path.join(basedir, 'download')
        path = os.path.join(download_dir, filename + '.scel')
        return path
