# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class BusinessinfotwoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
import threading,requests
import time
#from .spiders.beian_searchs import IcpRecard
from fake_useragent import UserAgent
from .utils_common.bloomfilter2 import BloomFilter

ips=[]
def buildList():
    while True:
        try:
            #if IcpRecard.flags == False:
                #break
            pro_addr = requests.get(
            'http://dynamic.goubanjia.com/dynamic/get/6f8e9b4dcc005b5077074fea55d55f56.html?sep=3').text
            ip = pro_addr.strip()

            if len(ips) == 0:
                ips.append(ip)
            else:
                ips[0] = ip
            time.sleep(6)
            print(ips, "22@")


        except Exception as e:
            print(e,"ip接口异常")

# th1 = threading.Thread(target=buildList)
# th1.start()
# th1.join()
#th1 = threading.Thread(target=buildList).start()

class MyUserAgentMiddleware(object):
    '''
    设置User-Agent
    '''
    def __init__(self):


        self.ua = UserAgent()
    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random


class HttpbinProxyMiddlewares(object):
    def __init__(self):

        self.th1 = threading.Thread(target=buildList).start()

        self.bf = BloomFilter()

    def process_request(self, request, spider):

        global ips

        if str(request.url).startswith('https://xin.baidu.com/detail/compinfo?'):
            if self.bf.isContains(request.url):  # 判断字符串是否存在
                print('url exists!{}'.format(request.url))
            else:
                ip = ips[0]
                print("开始使用IP({})请求： {}".format(ip, request.url))
                request.meta['proxy'] = 'http://' + ip

            if len(ips) == 0:
                return request
            else:
                ip = ips[0]
                print("开始使用IP({})请求： {}".format(ip, request.url))
                request.meta['proxy'] = 'http://' + ip
        else:
            ip = ips[0]
            print("开始使用IP({})请求： {}".format(ip, request.url))
            request.meta['proxy'] = 'http://' + ip


    def process_response(self, request, response, spider):
        global ips
        if response.status != 200:
            print("请求响应失败{},{},从新使用ip{}请求".format(response.status,response.url,ips[0]))
            # 对当前reque加上代理
            request.meta['proxy'] = 'http://' + ips[0]
            return request
        else:

            if str(response.url).startswith("https://xin.baidu.com/detail/compinfo?"):
                print('url not exists!{}'.format(response.url))
                self.bf.insert(response.url)
        return response
