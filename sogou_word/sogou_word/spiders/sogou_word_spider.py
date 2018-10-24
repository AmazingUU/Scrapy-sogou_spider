# -*- coding: utf-8 -*-
import scrapy


def get_cate2(response):
    cate1 = response.meta['cate1']

    # print(cate1)
    div_cate_no_child_list = response.xpath('//*[@class="cate_no_child no_select"]')
    div_cate_has_child_list = response.xpath('//*[@class="cate_has_child no_select"]')
    div_cate2_list = div_cate_no_child_list + div_cate_has_child_list

    print('total cate2 num:142,get cate2 num:',len(div_cate2_list))

class SogouWordSpiderSpider(scrapy.Spider):
    name = 'sogou_word_spider'
    # allowed_domains = ['https://pinyin.sogou.com/dict/cate/index/167']
    start_urls = ['http://pinyin.sogou.com/dict/cate/index/167/']

    def parse(self, response):
        cate1_list = ['城市信息', '自然科学', '社会科学', '工程应用', '农林渔畜', '医学医药', '电子游戏', '艺术设计', '生活百科', '运动休闲', '人文科学', '娱乐休闲']
        li_list = response.xpath('//*[@id="dict_nav_list"]/ul/li')
        for i in range(len(li_list)):
            url = 'http://pinyin.sogou.com' + li_list[i].xpath('./a/@href').extract()[0]
            print(url)
            yield scrapy.Request(url,callback=get_cate2,meta={'cate1':cate1_list[i]})
