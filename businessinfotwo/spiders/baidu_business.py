# # -*- coding: utf-8 -*-


import scrapy
import os,redis
#from businessinfo.businessinfo.utils_common.bloomfilter2 import BloomFilter
from ..utils_common.bloomfilter2 import BloomFilter
from urllib.parse import *
from ..utils_common.utils import Utils
from ..utils_common.long import Logger
import re,logging,time,execjs
from ..items import DomainItem,BaiduqiyeItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.utils.response import response_status_message
from lxml import etree
from ..settings import *
from tld import get_tld
class Baidu(scrapy.Spider):
    name = 'baidu_business'
    allowed_domains = ['baidu.com']

    'https://xin.baidu.com/s?q=%E6%96%B0%E7%BD%91%E6%95%B0%E7%A0%81&t=0'
    start_urls = [None]
    ip_code = True
    flags = True
    items = DomainItem()
    custom_settings = {"DEFAULT_REQUEST_HEADERS": {"Host": "xin.baidu.com", "referer": "https://xin.baidu.com/"}}
    utils = Utils()
    redis_connect = utils.connect_redis()
    # logyyx = Logger('long.log', logging.DEBUG, logging.DEBUG)

    handle_httpstatus_list = [403,302]


    def __init__(self):
        self.first_urls = 'https://xin.baidu.com/s/l?q={}&t=0&p={}&s=10&o=0&f=undefined&_={}'
    # self.start_urls = 'https://xin.baidu.com/s/l?q={}&t=0&p={}&s=10&o=0&f=undefined&_={}'
        self.start_page = 1
        self.domain = "https://xin.baidu.com"
        self.flag_one = True
        self.total_page_num = int(0)

    def start_requests(self):

        while True:
            keys = self.redis_connect.spop("beian")
            if keys:
                Logger.info("开始请求关键字：{}".format(keys))

                key = quote(keys)
                yield scrapy.Request(url=self.first_urls.format(key, self.start_page, int(time.time() * 1000)),callback=self.parse,errback=self.errback_httpbin,dont_filter=True,meta={"key":keys})



    def parse(self, response):
        key = response.meta.get("key", "")
        if response:

            if response.status==200:
                Logger.info("------------------------------")
                Logger.info("获取公司关键字列表：{}响应成功-状态：{}".format(response.meta.get("key",""),response.status))
                Logger.info("正在请求第：{}页成功-url:{}".format(self.start_page,response.url))
                Logger.info("------------------------------")
                s = response.text.replace("\\","")



                if self.flag_one==True:
                    self.flag_one = False
                    total_page_num = re.search(r'"totalPageNum":(\d+),',s,re.DOTALL)
                    if total_page_num:
                        try:
                            Logger.info("正在查看关键字key页数为：{}".format(self.start_page, ))
                            self.total_page_num = int(total_page_num.group(1))
                            # self.start_page = self.total_page_num
                        except Exception as e:
                            Logger.info("页码转换异常{}".format(e))

                partter = re.findall(r'''<a class="zx-list-item-url".*?target="_blank".*?href=.*?title=.*?>''',s,re.DOTALL)


                if len(partter) ==0:
                    return False
                else:
                    url_list = [re.search('.*?href="(.*?)" title=.*?', x).group(1) for x in partter]

                    if url_list:
                        print(url_list, 3306)
                        for url in url_list:
                            yield scrapy.Request(url=self.domain+url,callback=self.parse1, errback=self.errback_httpbin,meta={"first_url":self.domain+url}, dont_filter=True)


                    if url_list:
                        Logger.info("获取列表信息成功")
                    if self.start_page < self.total_page_num:
                        self.start_page+=1
                        # url_list = self.start_list_page_url()
                        Logger.info("正在向上翻第{}页：".format(self.start_page))
                        yield scrapy.Request(url=self.first_urls.format(key, self.start_page, int(time.time() * 1000)),callback=self.parse, errback=self.errback_httpbin, dont_filter=True,meta={"key": key})


                    else:
                        Logger.info("翻页结束进行下一轮关键字爬取")



    def parse1(self,response):
        if response:
            if response.status==200:
                Logger.info("返回详情页信息成功")
                pid, tk, time1 = self.analysis_detail_paramenter(response)
                url1 = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
                yield scrapy.Request(url=url1,callback=self.parse2, errback=self.errback_httpbin, dont_filter=False,)
                time.sleep(1)


    def parse2(self,response):
        print("sfsfsfsf")
        if response:
            if response.status == 200:
                null = ""
                true = True

                # dict_str = response.text.replace("\\", "").replace(" ","").replace(
                #     "\n", "").replace("\t", "")
                dict_str =response.text
                item = BaiduqiyeItem()
                dict_type = eval(dict_str).get("data")


                item["company_introduce"] = dict_type.get("company_introduce", "")
                item["tel"] = dict_type.get("telephone", "")
                item["contacts_people"] = dict_type.get("contacts_people", "")
                item["m_phone"] = dict_type.get("m_phone", "")
                item["company_name"] = dict_type.get("entName", "")
                item["status"] = dict_type.get("openStatus", "")
                item["company_type"] = dict_type.get("entType", "")
                item["establish_date"] = dict_type.get("startDate", "")
                item["expire_date"] = dict_type.get("openTime", "")
                item["register_money"] = dict_type.get("regCapital", "")
                item["register_authority"] = dict_type.get("annualDate", "")
                item["business_scope"] = dict_type.get("scope", "")
                item["register_address"] = dict_type.get("regAddr", "")
                item["legal_representative"] = dict_type.get("legalPerson", "")
                item["register_num"] = dict_type.get("regNo", "")
                item["company_website"] = dict_type.get("company_website", "")
                item["area_p"] = dict_type.get("area_p", 0)
                item["area_s"] = dict_type.get("area_s", 0)
                item["area_q"] = dict_type.get("area_q", 0)
                item["industry_id"] = 0
                item["industry"] = dict_type.get("industry", "")
                print(item,"444444444444444444444444444444444444444444444444444444444")
                yield item
                # if item["company_name"]:
                #     Baidu.utils.insertMysql(item, Logger)
                #
                #     flag2 = Baidu.utils.insertEs(item)
                #     if flag2 == True:
                #         Logger.info("insert es seccess")
                #     elif flag2 == False:
                #         Logger.info("insert es exist")
                #     elif "插入es异常" in flag2:
                #         Logger.info(flag2)






    def analysis_detail_paramenter(self,r_detail):

        text = r_detail.text

        # reponse = r_detail.content.decode()
        html = etree.HTML(text)
        d = html.xpath('//*[@id="baiducode"]/text()')[0]
        pid = eval(re.findall(r'"pid":(.*?)\,.*?"defTags"', text, re.S)[0])
        id1, att = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", text)[0]
        tk_func = "function mix(" + re.findall(r'mix\((.*?)\(function', text, re.S)[0]
        tk = re.findall(att + r'="(.*?)"\>', text)[0]
        tk = execjs.compile(tk_func).call('mix', tk, d)
        time1 = int(time.time() * 1000)
        return pid,tk,time1


    def errback_httpbin(self, failure):

        print(repr(failure))

        if failure.check(HttpError):

            response = failure.value.response
            Logger.error("httperror:{}".format(response.url))

            # self.logger.error('HttpError on %s', response.url)
            yield scrapy.Request(url=response.url, callback=self.parse, errback=self.errback_httpbin)
        elif failure.check(DNSLookupError):

            request = failure.request
            Logger.error("DNSLookupError:{}".format(request.url))
            # self.logger.error('DNSLookupError on %s', request.url)
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            Logger.error("TimeoutError on:{}".format(request.url))
            # self.logger.error('TimeoutError on %s', request.url)
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)
        else:
            request = failure.request
            Logger.error("qita:{}".format(repr(failure)))
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)

