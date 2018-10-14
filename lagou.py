import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from lxml import etree


browser = webdriver.Chrome()

def get_detail_page(url):
    try:
        browser.get(url)
        # 等待页面加载完成
        WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#s_position_list > ul > li.con_list_item.first_row.default_list > div.list_item_top > div.position > div.p_top > a'))
        )
        source = browser.page_source
        html = etree.HTML(source)
        detail_urls = html.xpath('//a[@class="position_link"]/@href')
        for detail_url in detail_urls:
            parse_detail_page(detail_url)
    except TimeoutException:
        print('请求超时,重新请求页面')
        get_detail_page(url)

def parse_detail_page(url):
    try:
        browser.get(url)
        source = browser.page_source
        html = etree.HTML(source)
        WebDriverWait(browser,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'position-head'))
        )
        positionName = html.xpath('//div[@class="job-name"]/@title')[0]
        dd = html.xpath('//dd[@class="job_request"]//span/text()')
        if len(dd) > 4:
            salary = dd[0]
            city = dd[1].replace('/','').strip()
            workYear = dd[2].replace('/','').strip()
            education = dd[3].replace('/','').strip()
        job = {
            '职位': positionName,
            '薪水': salary,
            '城市': city,
            '工作经验': workYear,
            '教育经历': education
        }
        save_to_txt(job)
    except TimeoutException:
        print('请求超时')

def save_to_txt(content):
    with open('job.txt', 'a') as f:
        print('正在保存职位信息:', content)
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main():
    url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
    get_detail_page(url)

if __name__ == '__main__':
    main()