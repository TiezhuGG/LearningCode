
import os
import time
import requests
from lxml import etree
import random
from multiprocessing import Pool


UAPOOLS = [
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
]

HEADERS = {
    'User-Agent': random.choice(UAPOOLS)
}

def get_img_url(url):
    try:
        response = requests.get(url,headers=HEADERS)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            imgs_url = html.xpath('//div[@class="page-content text-center"]//img/@data-original')
            return imgs_url
        return None
    except requests.ConnectionError:
        print('请求页面失败.')

def parse_img(img_url):
    try:
        response = requests.get(img_url,headers=HEADERS,timeout=10)
        if response.status_code == 200:
            html = response.content
            save_image(img_url,html)
    except requests.exceptions.ReadTimeout:
        print('请求图片页面失败..')
        return None

def save_image(img_url,html):
    path = os.path.join('/home/lihongfa/Desktop/21DaysWS/','images')
    if not os.path.exists(path):
        os.mkdir(path)
    img_name = img_url.split('/')[-1]
    img_path = os.path.join(path,img_name)
    if not os.path.exists(img_path):
        with open(img_path,'wb') as f:
            f.write(html)
            print('正在保存图片:', img_name)
            f.close()

def main():
    urls = []
    for x in range(1,6):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(x)
        imgs_url = get_img_url(url)
        if imgs_url:
            for img_url in imgs_url:
                urls.append(img_url)

    pool = Pool()
    pool.map(parse_img,urls)
    pool.close()
    pool.join()


if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print('Cost time:', (e-s))