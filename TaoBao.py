#! /usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from urllib.parse import quote

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
# 搜索关键词
KEYWORD = 'iPad'


def index_page(page):
    '''
        抓取商品索引页:
        page: 页码
    '''
    print('正在爬取第', page, '页')
    try:
        url = 'http://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            # 等待页码输入框和确定按钮加载出来
            _input = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input'))
            )[0]
            submit = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit'))
            )[0]
            _input.clear()
            _input.send_keys(page)
            submit.click()
        # 验证输入的页码与当前页码是否一致的等待条件，如果是，就证明页面跳转成功
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page))
        )
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item'))
        )
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    '''
        提取商品数据
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc(
        '#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
#         save_to_mongo(product)

def main():
    '''
        遍历多页
    '''
    for i in range(1, 101):
        index_page(i)


if __name__ == '__main__':
    main()
