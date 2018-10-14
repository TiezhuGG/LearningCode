# -*- conding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random
from requests.exceptions import RequestException
import json
import time
import redis
import pymysql
import pymongo

UAPOOLS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    ]

headers = {
    'User-Agent': random.choice(UAPOOLS),
    'Host': 'www.qidian.com'
}
#创建redis数据库连接
rconn = redis.Redis('192.168.xxx.xxx','6379')

#创建mongodb数据库连接
mongo_uri = '192.168.xxx.xxx:27017'
client = pymongo.MongoClient(mongo_uri)
db = client['qidian']
collection = db['novel']

def get_infos(url):
    response = requests.get(url,headers=headers)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'lxml')
            lis = soup.select('div.book-img-text > ul > li')
            for li in lis:
                title = li.select('h4 > a')[0].string
                author = li.select('p.author > a')[0].string
                type = li.select('p.author > a')[1].string + '-' + li.select('p.author > a')[2].string
                updating = li.select('p.author > span')[0].string
                # intro = li.find_all('p',class_="intro")
                novel = {
                    'title': title,
                    'author': author,
                    'type': type,
                    'updating': updating
                }
                print('Loading >>> %s' % novel + '\n')
                time.sleep(0.25)

                #插入数据
                collection.insert_one(novel)
        return None
    except RequestException:
        print('Request Error')

def main():
    for page in range(1,21):
        url = 'https://www.qidian.com/all?page={}'.format(page)
        rconn.sadd('urls',url)

    pop_url = rconn.spop('urls')
    if pop_url:
        while pop_url:
            print('=' * 80)
            print("Crawling>>>>>>>>>", pop_url)
            print('=' * 80)
            get_infos(pop_url)
            pop_url = rconn.spop('urls')
    else:
        print('Done...')
        # db.close()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('Cost Time %s:' % (end-start))
