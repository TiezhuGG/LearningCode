# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import JianshuItem


class JsSpiderSpider(CrawlSpider):
    name = 'js_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[a-z0-9]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        item = JianshuItem()
        item['title'] = response.xpath('//h1[@class="title"]/text()').get()
        item['avatar'] = response.xpath('//a[@class="avatar"]/img/@src').get()
        item['author'] = response.xpath('//span[@class="name"]/a/text()').get()
        item['pub_time'] = response.xpath('//span[@class="publish-time"]/text()').get()
        item['origin_url'] = response.url
        item['article_id'] = response.url.split('/')[-1]
        item['content'] = response.xpath('//div[@class="show-content-free"]').get()
        yield item