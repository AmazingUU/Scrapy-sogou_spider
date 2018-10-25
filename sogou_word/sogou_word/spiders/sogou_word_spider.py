# -*- coding: utf-8 -*-
import scrapy

from sogou_word.items import SogouWordItem


def strip(title):
    res = ''
    char_list = ['\\','/',':','*','?','"','<','>','|']
    for char in title:
        if char not in char_list:
            res += char
    return res

def get_download(response):
    item = SogouWordItem()
    cate1 = response.meta['cate1']
    cate2 = response.meta['cate2']

    div_detail_block_list = response.xpath('//*[@class="dict_detail_block"]')
    div_detail_block_odd_list = response.xpath('//*[@class="dict_detail_block odd"]')
    div_detail_list = div_detail_block_list + div_detail_block_odd_list
    for div in div_detail_list:
        title = div.xpath('./div[1]/div/a/text()').extract()[0]
        item['url'] = div.xpath('./div[2]/div[2]/a/@href').extract()[0]
        item['filename'] = '{}_{}_{}'.format(cate1,cate2,strip(title))
        item['cate1'] = cate1
        item['cate2'] = cate2
        yield item

def get_detail(response):
    cate1 = response.meta['cate1']
    cate2 = response.meta['cate2']
    url = response.meta['url']

    li_list = response.xpath('//*[@id="dict_page_list"]/ul/li')
    try:
        page_num = li_list[-2].xpath('./span/a/text()').extract()[0]
    except:
        page_num = 1
    # print(page_num)
    for i in range(1,int(page_num) + 1):
        link = url + '/default/' + str(i)
        yield scrapy.Request(link,callback=get_download,meta={'cate1':cate1,'cate2':cate2},dont_filter=True)

def get_cate2(response):
    cate1 = response.meta['cate1']
    # print(cate1)
    div_cate_no_child_list = response.xpath('//*[@class="cate_no_child no_select"]')
    div_cate_has_child_list = response.xpath('//*[@class="cate_has_child no_select"]')
    div_cate2_list = div_cate_no_child_list + div_cate_has_child_list
    # print('total cate2 num:142,get cate2 num:',len(div_cate2_list))
    for div in div_cate2_list:
        cate2_list = div.xpath('./a//text()').extract()
        cate2 = cate2_list[0] + cate2_list[1]
        # print(cate2)
        url = 'http://pinyin.sogou.com' + div.xpath('./a/@href').extract()[0]
        yield scrapy.Request(url,callback=get_detail,meta={'cate1':cate1,'cate2':cate2,'url':url},dont_filter=True)

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
