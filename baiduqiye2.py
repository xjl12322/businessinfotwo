#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import requests,time,execjs,re,grequests,asyncio
from lxml import etree
from urllib import parse
from ip import getip
from long import Logger
from urllib.parse import quote
from utils import Utils
import logging,threading
from ast import literal_eval
from multiprocessing import Queue
class BaiduQiye(object):
    utils = Utils()
    logyyx = Logger('long.log', logging.DEBUG, logging.DEBUG)
    def __init__(self):
        self.q = Queue()

        self.header = {
            "Host": "xin.baidu.com",
            "referer": "https://xin.baidu.com/",
            "USER_AGENT": 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'
        }
        self.start_urls = 'https://xin.baidu.com/s/l?q={}&t=0&p={}&s=10&o=0&f=undefined&_={}'
        self.start_page = 1
        self.domain = "https://xin.baidu.com"
        self.flag_one = True
        self.total_page_num = int(0)
        self.ips = None

    def request_url_list(self,url):
        try:
            urls = url
            r = requests.get(url=urls,headers=self.header,proxies = self.ips,timeout=16,allow_redirects=False)
            r.encoding = "utf-8"
            return r
        except Exception as e:
            self.ips = getip()
            BaiduQiye.logyyx.info("请求异常{}-继续使用代理ip:{}".format(e,self.ips))
            # self.start_list_page_url()
            self.request_url_list(url)

    def start_list_page_url(self,key):
        keys = quote(key)
        r = self.request_url_list(self.start_urls.format(keys,self.start_page,int(time.time() * 1000)))

        # BaiduQiye.logyyx.info("正在请求第：{}页".format(self.start_page))
        # BaiduQiye.logyyx.info("23333333333333333{}".format(r.status_code))
        # BaiduQiye.logyyx.info(r.url)
        if r:
            if r.status_code==200:
                BaiduQiye.logyyx.info("响应状态码：{}--响应连接：{}".format(r.status_code,r.url))
                BaiduQiye.logyyx.info("正在请求第：{}页成功".format(self.start_page))
                s = r.text.replace("\\","")
                partter = re.findall(r'''<a class="zx-list-item-url".*?target="_blank".*?href=.*?title=.*?>''',s,re.DOTALL)
                if len(partter) ==0:
                    return False
                else:
                    BaiduQiye.logyyx.info("676767767676")
                    url_list = [re.search('.*?href="(.*?)" title=.*?', x).group(1) for x in partter]
                    if url_list:
                        return url_list
            else:
                self.ips = getip()
                BaiduQiye.logyyx.info("ip被封 使用代理ip:{}".format(self.ips))
                self.start_list_page_url(key)
                # print(partter)

        else:
            BaiduQiye.logyyx.info("响应失败：状态码{}--响应连接：{}".format(r.status_code, r.url))
    # def start_list_page_url2(self,partter):




    # def grequests_detail_page(self,url_list):
    #     list_url = [grequests.get(self.domain+x, headers=self.header) for x in url_list]
    #     response_detail = grequests.map(list_url, size=1)
    #     return response_detail
    def requests_detail_page(self,url):
        response_detail = self.request_url_list(self.domain+url)
        return response_detail

    def analysis_detail_paramenter(self,r_detail):

        text = r_detail.text
        reponse = r_detail.content.decode()
        html = etree.HTML(reponse)
        d = html.xpath('//*[@id="baiducode"]/text()')[0]
        pid = eval(re.findall(r'"pid":(.*?)\,.*?"defTags"', text, re.S)[0])
        id1, att = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", text)[0]
        tk_func = "function mix(" + re.findall(r'mix\((.*?)\(function', text, re.S)[0]
        tk = re.findall(att + r'="(.*?)"\>', text)[0]
        tk = execjs.compile(tk_func).call('mix', tk, d)
        time1 = int(time.time() * 1000)
        return pid,tk,time1


    def extract_json(self,pid,tk,time1):
        true = True
        url1 = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
        resp1 = requests.get(url1, headers=self.header)
        dict_str = resp1.content.decode('unicode_escape').replace("\\","").replace(" ","").replace("\n","").replace("\t","")
        dict_type = eval(dict_str).get("data")

        item = {}
        item["company_introduce"] = dict_type.get("company_introduce","")
        item["tel"] = dict_type.get("telephone","")
        item["contacts_people"] = dict_type.get("contacts_people","")
        item["m_phone"] = dict_type.get("m_phone","")
        item["company_name"] = dict_type.get("entName","")
        item["status"] = dict_type.get("openStatus","")
        item["company_type"] = dict_type.get("entType","")
        item["establish_date"] = dict_type.get("startDate","")
        item["expire_date"] = dict_type.get("openTime","")
        item["register_money"] = dict_type.get("regCapital","")
        item["register_authority"] =dict_type.get("annualDate","")
        item["business_scope"] = dict_type.get("scope","")
        item["register_address"] = dict_type.get("regAddr","")
        item["legal_representative"] = dict_type.get("legalPerson","")
        item["register_num"] = dict_type.get("regNo","")
        item["company_website"] = dict_type.get("company_website","")
        item["area_p"] = dict_type.get("area_p",0)
        item["area_s"] = dict_type.get("area_s",0)
        item["area_q"] = dict_type.get("area_q",0)
        item["industry_id"] = 0
        item["industry"] = dict_type.get("industry","")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return item





    @staticmethod
    def app():

        baiduqiye = BaiduQiye()
        BaiduQiye.logyyx.info("程序初始化")
        BaiduQiye.logyyx.info("程序开始启动")

        # r = baiduqiye.request_url_list()
        r = BaiduQiye.utils.connect_redis()
        key = r.spop("beian")
        if key:
            url_list = baiduqiye.start_list_page_url(key)
            BaiduQiye.logyyx.info("获取公司相关信息成功")
            if url_list:
                for url in url_list:
                    BaiduQiye.logyyx.info("开始请求公司详情页")
                    response_detail = baiduqiye.requests_detail_page(url)
                    if response_detail:
                        BaiduQiye.logyyx.info("返回详情页响应成功")
                # for r_detail in list(response_detail):
                    # print(r_detail)
                    # r_detail.status_code
                        pid, tk, time1 = baiduqiye.analysis_detail_paramenter(response_detail)
                        item = baiduqiye.extract_json(pid, tk, time1)
                        print(item,"3306")
                        BaiduQiye.logyyx.info("解析数据信息成功")
                    #
                        if item["company_name"]:
                            BaiduQiye.utils.insertMysql(item,BaiduQiye.logyyx)

                            flag2= BaiduQiye.utils.insertEs(item)
                            if flag2 == True:
                                BaiduQiye.logyyx.info("insert es seccess")
                            elif flag2 == False:
                                BaiduQiye.logyyx.info("insert es exist")
                            elif "插入es异常" in flag2:
                                BaiduQiye.logyyx.info(flag2)

        else:
            BaiduQiye.logyyx.info("redis 集合返回空")

if __name__ =="__main__":

    BaiduQiye.app()

















# print("___________________")
#
#
# selector = etree.HTML(r.text)
# list_urls = selector.xpath('//div[@class="zx-list-wrap"]//div[@class="zx-ent-logo"]/a/@href')
#
#
#
#
#
# list_url = [grequests.get(parse.urljoin(r.url,x),headers = header)for x in list_urls]
# response_list = grequests.map(list_url,size=2)
# print(response_list)
#
# for r_detail in response_list:
#     print(r_detail.status_code)
#     print(r_detail.url)
#     text = r_detail.text
#
#
#     # print(r_detail.text)
#     reponse = r_detail.content.decode()
#     html2 = etree.HTML(reponse)
#     d = html2.xpath('//*[@id="baiducode"]/text()')[0]
#     pid = eval(re.findall(r'"pid":(.*?)\,.*?"defTags"', text, re.S)[0])
#     id1, att = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", text)[0]
#     tk_func = "function mix(" +re.findall(r'mix\((.*?)\(function', text,re.S)[0]
#     print(tk_func)
#     tk = re.findall(att + r'="(.*?)"\>', text)[0]
#     print(tk, d)
#     tk = execjs.compile(tk_func).call('mix', tk, d)
#     print(tk)
#     time1 = int(time.time() * 1000)
#     url1 = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
#     resp1 = requests.get(url1, headers=header)
#     print(resp1.content.decode('unicode_escape'))
#     print(type(resp1.content.decode('unicode_escape')))
#
#
#
#
#
# print("222")


#
# print(list_url,"list")
# for x in list_urls:
#     url = parse.urljoin(r.url,x)
#     logyyx.info("请求url：{}".format(url))
#     time.sleep(5)
#     r_detail = requests.get(url=url,headers=header)
#     text = r_detail.text
#     print(r_detail.status_code)
#     # print(r_detail.text)
#     reponse = r_detail.content.decode()
#     html2 = etree.HTML(reponse)
#     d = html2.xpath('//*[@id="baiducode"]/text()')[0]
#     pid = eval(re.findall(r'"pid":(.*?)\,.*?"defTags"', text, re.S)[0])
#     id1, att = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", text)[0]
#     tk_func = "function mix(" +re.findall(r'mix\((.*?)\(function', text,re.S)[0]
#     print(tk_func)
#     tk = re.findall(att + r'="(.*?)"\>', text)[0]
#     print(tk, d)
#     tk = execjs.compile(tk_func).call('mix', tk, d)
#     print(tk)
#     time1 = int(time.time() * 1000)
#     url1 = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
#     resp1 = requests.get(url1, headers=header)
#     print(resp1.content.decode('unicode_escape'))
#     print(type(resp1.content.decode('unicode_escape')))








