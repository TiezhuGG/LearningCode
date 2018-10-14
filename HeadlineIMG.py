#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import json
from urllib.parse import urlencode
from requests import RequestException
import os
from urllib import request
from multiprocessing import Pool


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.weiwei; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
}

keyword = '海贼王'
def get_detail_page(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            text = response.text
            data = json.loads(text)
            # 分析网页结构,提取详情页面url
            if data and 'data' in data.keys():
                for obj in data.get('data'):
                    detail_url = obj.get('article_url')
                    # 有详情页的话,返回一个生成器等待调用
                    if detail_url:
                        yield detail_url
        return None
    except RequestException:
        return None

def parse_detail_page(url,keyword):
    response = requests.get(url,headers=headers)
    text = response.text
    title = re.findall(r'<title>(.*?)</title>',text,re.S)
    result = re.findall('gallery: JSON.parse\((.*?)\),',text,re.S)
    if title and result:
        for str in result:
            # 此处分析网页源代码,需要json.loads两次
            str_json = json.loads(str)
            data = json.loads(str_json)
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                # 下载图片
                for image in images:
                    download_image(image,keyword)
                return  {
                    'title': title,
                    'images': images
                }

def download_image(url,keyword):
    print('正在下载图片%s' % url)
    filename = url.split('/')[-1] + '.jpg'    # 文件名
    image_path = os.path.join(os.path.dirname(__file__),keyword)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    request.urlretrieve(url,os.path.join(image_path,filename))      # 拼接好存储路径,以文件名存储

def main(offset):
    detail_urls = get_detail_page(offset,keyword)
    for detail_url in detail_urls:
        parse_detail_page(detail_url,keyword)

if __name__ == '__main__':
    # for i in range(1):
    #     main(i*20)
    pool = Pool()
    pool.map(main,[x*20 for x in range(30)])
    pool.close()
    pool.join()
