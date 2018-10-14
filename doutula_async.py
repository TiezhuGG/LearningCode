import aiohttp
import asyncio
import time
from urllib import request
import random
from lxml import etree
import re
import os

UAPOOLS = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    ]
async def get_imgs(url):
    headers = {
        "User-Agent": random.choice(UAPOOLS)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as response:
            text = await response.text()
            html = etree.HTML(text)
            imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
            for img in imgs:
                img_url = img.get('data-original')
                alt = img.get('alt')
                alt = re.sub(r'[\\/?、~!！.，,。]', '', alt)
                filename = alt + img_url[-4:]
                async with session.get(img_url,headers=headers) as img_response:
                    content = await img_response.read()
                    img_path = os.path.dirname(__file__) + '/images/'
                    if not os.path.exists(img_path):
                        os.mkdir(img_path)
                    with open(img_path+filename,'wb') as f:
                        print('%s is loading...' % filename)
                        f.write(content)
                        f.close()

if __name__ == '__main__':
    urls = []
    for page in range(1,6):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(page)
        urls.append(url)

    start = time.time()
    tasks = [get_imgs(url) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print('cost time:',end-start)
