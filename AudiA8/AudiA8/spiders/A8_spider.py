# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractor import LinkExtractor
from ..items import Audia8Item


class A8SpiderSpider(CrawlSpider):
    name = 'A8_spider'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/146.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/146.+'),callback='crawler',follow=True),
    )

    def crawler(self, response):
        item = Audia8Item()
        item['category'] = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]/ text()').extract_first()
        urls = response.xpath('//div[@class="uibox-con carpic-list03 border-b-solid"]/ul/li//img/@src').extract()
        # 构造image_urls
        item['image_urls'] = list(map(lambda url: response.urljoin(url.replace('t_', '')), urls))
        yield item
