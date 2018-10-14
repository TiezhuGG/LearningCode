import requests
import random
from lxml import etree
import time


UAPOOLS = [
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
]

HEADERS = {
    'User-Agent': random.choice(UAPOOLS),
    'Referer': 'https://github.com/login',
    'Host': 'github.com'
}


class SignIn():
    def __init__(self):
        self.login_url = 'https://github.com/login'
        self.session_url = 'https://github.com/session'
        self.session = requests.Session()

    def get_token(self):
        try:
            response = self.session.get(self.login_url,headers=HEADERS)
            if response.status_code == 200:
                html = etree.HTML(response.text)
                token = html.xpath('//input[@name="authenticity_token"]/@value')[0]
                return token
        except requests.ConnectionError:
            print('请求github登录页面失败..')
            return None

    def login(self,email,password):
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.session_url,headers=HEADERS,data=data)
        print('='*80)
        print(response.url)
        if response.status_code == 200:
            self.after_logined(response.text)


    def after_logined(self,html):
        selector = etree.HTML(html)
        name = selector.xpath('//strong[@class="css-truncate-target"]/text()')[0]
        #print(name)
        if name == "TiezhuGG":
            print('登录github成功')
        else:
            print('登录失败')


if __name__ == '__main__':
    login = SignIn()
    login.login(email=email,password=password)



