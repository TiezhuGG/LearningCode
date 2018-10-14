'''
    使用PhantomJS爬取腾讯动漫
'''

from selenium import webdriver
import re
from urllib import  request
import time
import os

def parse_page(url):
    browser = webdriver.PhantomJS()
    # browser = webdriver.Chrome()
    browser.get(url)
    # 自动向下滑动到底部
    length = 1200
    for i in range(10):
        browser.execute_script('window.scrollTo(0,%s)' % length)
        time.sleep(0.5)
        length += length


    html = browser.page_source
    # 将网页源代码写入文件
    with open('dongman.txt','w',encoding='utf-8') as f:
        f.write(html)
        f.close()
    browser.quit()

    image_urls = re.findall('<img src="(https://manhua.qpic.cn/manhua_detail/.*?.jpg/0)"',html,re.S)
    # print(image_urls)
    for i in range(len(image_urls)):
        image_url = image_urls[i]
        file_path = '第%s章' % url.split('/')[-1]
        filename = str(i) + '.jpg'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        os.chdir(file_path)
        request.urlretrieve(image_url,filename)
        os.chdir('D:\新建文件夹\PycharmProjects\天善爬虫课程\weiwei\images')

def main():
    for page in range(1,5):
        print('正在爬取第%s页' % page)
        url = 'http://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page)
        parse_page(url)

if __name__ == '__main__':
    main()




