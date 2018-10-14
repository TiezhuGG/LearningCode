# -*- coding: utf-8 -*-
import scrapy
from PIL import Image
from urllib import request

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.douban.com']
    # start_urls = ['https://accounts.douban.com/login']

    login_url = 'https://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/159166942/'
    signature_url = 'https://www.douban.com/j/people/159166942/edit_signature'

    def start_requests(self):
        yield scrapy.Request(self.login_url,callback=self.login,dont_filter=True)

    def login(self, response):
        print('请登录:',response.url)
        data = {
            'source': 'index_nav',
            'redir': 'https://www.douban.com/',
            'form_email': '13559422200',
            'form_password': 'lhf101400',
            'remember': 'on',
            'login': '登录'
        }
        captcha_url = response.xpath('//img[@id="captcha_image"]/@src').get()
        if captcha_url:
            print('captcha_url:',captcha_url)
            request.urlretrieve(captcha_url, 'captcha.png')
            captcha = input('请输入验证码:')
            # captcha = self.captcha_image(captcha_url)
            data['captcha-solution'] = captcha
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').get()
            data['captcha-id'] = captcha_id
        yield scrapy.FormRequest(self.login_url,formdata=data,callback=self.enter_profile,dont_filter=True)

    def enter_profile(self, response):
        print(response.status)
        if response.status == 200:
            print('登录成功,当前页面为:',response.url)
            yield scrapy.Request(self.profile_url,callback=self.enter_signature)
        else:
            print('登录失败了...')

    def enter_signature(self,response):
        print(response.status)
        if response.status == 200:
            print('进入到个人首页:',response.url)
            ck = response.xpath('//input[@name="ck"]/@value').get()
            data = {
                'ck': ck,
                'signature': '女神身边的绝世蹩脚货...'
            }
        yield scrapy.FormRequest(self.signature_url,formdata=data,callback=self.return_none)

    # 因为enter_signature若没有指定回调函数的话,会默认返回执行parse函数
    # 所以声明了return_none函数,使程序不会再进入到parse函数
    def return_none(self,response):
        print('End...')


    # def captcha_image(self,captcha_url):
    #     request.urlretrieve(captcha_url,'captcha.png')
    #     image = Image.open('captcha.png')
    #     image.show()
    #     captcha = input('请输入验证码:')
    #     return captcha