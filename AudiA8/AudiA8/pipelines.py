# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from scrapyproject.AudiA8.AudiA8 import settings

# 使用scrapy内置ImagesPipeline下载图片
class A8ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['image_urls']:
            yield Request(img_url,meta={'item':item})

    # 自定义图片存储路径
    def file_path(self, request, response=None, info=None):
        # 通过request对象得到image_url
        image_url = request.url
        # 通过request的meta参数得到item中的category
        category = request.meta['item']['category']
        # 构造图片存储路径: /images_store/category/image_name
        image_name = image_url.split('/')[-1]
        images_store = settings.IMAGES_STORE
        image_path = os.path.join(category,image_name)
        return image_path
