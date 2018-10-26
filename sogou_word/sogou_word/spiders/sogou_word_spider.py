# -*- coding: utf-8 -*-
import scrapy

from sogou_word.items import SogouWordItem


def strip(title):  # 去除文件名中不符合文件名规则的字符
    res = ''
    char_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in title:
        if char not in char_list:
            res += char
    return res


def get_download(response):  # 获取下载url和标题
    item = SogouWordItem()
    cate1 = response.meta['cate1']
    cate2 = response.meta['cate2']

    div_detail_block_list = response.xpath('//*[@class="dict_detail_block"]')
    div_detail_block_odd_list = response.xpath('//*[@class="dict_detail_block odd"]')
    div_detail_list = div_detail_block_list + div_detail_block_odd_list
    for div in div_detail_list:
        title = div.xpath('./div[1]/div/a/text()').extract()[0]
        item['url'] = div.xpath('./div[2]/div[2]/a/@href').extract()[0]
        item['filename'] = '{}_{}_{}'.format(cate1, cate2, strip(title))
        item['cate1'] = cate1
        item['cate2'] = cate2
        yield item


def get_detail(response):  # 获取每一个二级分类的页数
    cate1 = response.meta['cate1']
    cate2 = response.meta['cate2']
    url = response.meta['url']

    li_list = response.xpath('//*[@id="dict_page_list"]/ul/li')
    try:
        # li_list[-1]为下一页，[-2]即为总页数
        page_num = li_list[-2].xpath('./span/a/text()').extract()[0]
    except:
        page_num = 1  # 只有一页才会报数组越界异常
    for i in range(1, int(page_num) + 1):
        # 将页数和原url组合成新的url才是包含所有词库的url
        link = url + '/default/' + str(i)
        yield scrapy.Request(link, callback=get_download, meta={'cate1': cate1, 'cate2': cate2}, dont_filter=True)


def get_cate2(response):  # 获取二级分类的相关信息
    cate1 = response.meta['cate1']
    # 没有再细化分的二级分类标签列表，例如:"自然科学"里的数学
    div_cate_no_child_list = response.xpath('//*[@class="cate_no_child no_select"]')
    # 有细化分的二级分类标签列表,例如:"自然科学"里的物理
    div_cate_has_child_list = response.xpath('//*[@class="cate_has_child no_select"]')
    div_cate2_list = div_cate_no_child_list + div_cate_has_child_list
    for div in div_cate2_list:
        cate2_list = div.xpath('./a//text()').extract()
        # 将二级分类标题和数字组合，例:风景名胜(4)
        cate2 = cate2_list[0] + cate2_list[1]
        url = 'http://pinyin.sogou.com' + div.xpath('./a/@href').extract()[0]
        yield scrapy.Request(url, callback=get_detail, meta={'cate1': cate1, 'cate2': cate2, 'url': url},
                             dont_filter=True)


class SogouWordSpiderSpider(scrapy.Spider):
    name = 'sogou_word_spider'
    # allowed_domains = ['https://pinyin.sogou.com/dict/cate/index/167']
    start_urls = ['http://pinyin.sogou.com/dict/cate/index/167/']

    def parse(self, response):
        # 这里一级分类的文字信息爬取不到，因为网页上一级分类名称是图片上的文字，所以直接就写死这十二类了
        cate1_list = ['城市信息', '自然科学', '社会科学', '工程应用', '农林渔畜', '医学医药', '电子游戏', '艺术设计', '生活百科', '运动休闲', '人文科学', '娱乐休闲']
        li_list = response.xpath('//*[@id="dict_nav_list"]/ul/li')
        # 获取一级分类的相关信息
        for i in range(len(li_list)):
            url = 'http://pinyin.sogou.com' + li_list[i].xpath('./a/@href').extract()[0]
            yield scrapy.Request(url, callback=get_cate2, meta={'cate1': cate1_list[i]})
