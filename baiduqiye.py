#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import requests,time,execjs,re,grequests,asyncio
from lxml import etree
from urllib import parse

from long import Logger
from urllib.parse import quote
from utils import Utils
import logging,threading
from multiprocessing import Queue




# ips=dict()
ips = []
def getip():
    global ips
    while True:

        try:
            pro_addr = requests.get(
        'http://dynamic.goubanjia.com/dynamic/get/6f8e9b4dcc005b5077074fea55d55f56.html?sep=3').text
            ip = pro_addr.strip()

            # ips["https"] = ip

            if len(ips) == 0:
                ips.append(ip)
            else:
                ips[0] = ip
            print(ips,1)
            time.sleep(4)
        except Exception as e:
            print(e, "ip接口异常")
p1 = threading.Thread(target=getip)
p1.start()
time.sleep(3)

class BaiduQiye(object):
    utils = Utils()
    logyyx = Logger('long.log', logging.DEBUG, logging.DEBUG)
    def __init__(self):
        self.q = Queue()
        # self.c = threading.Thread(target=getip).start()
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
        self.ip = ips


    def request_url_list(self,url):
        try:
            urls = url
            r = requests.get(url=urls,headers=self.header,proxies = self.ip,timeout=16,allow_redirects=False)
            r.encoding = "utf-8"
            return r

        except Exception as e:
            global ips
            self.ip = ips
            BaiduQiye.logyyx.info("请求异常{}-继续使用代理ip:{} 请求url：{}".format(e,self.ip,url))
            # self.start_list_page_url()
            self.request_url_list(url)
        print(ips, "xjl123322")
    def start_list_page_url(self,key):
        keys = quote(key)
        r = self.request_url_list(self.start_urls.format(keys,self.start_page,int(time.time() * 1000)))


        # BaiduQiye.logyyx.info("正在请求第：{}页".format(self.start_page))
        # BaiduQiye.logyyx.info("23333333333333333{}".format(r.status_code))
        # BaiduQiye.logyyx.info(r.url)
        if r:

            if r.status_code==200:
                BaiduQiye.logyyx.info("------------------------------")
                BaiduQiye.logyyx.info("获取公司关键字列表：{}响应成功-状态：{}".format(key,r.status_code))
                BaiduQiye.logyyx.info("正在请求第：{}页成功-url:{}".format(self.start_page,r.url))
                BaiduQiye.logyyx.info("------------------------------")
                s = r.text.replace("\\","")

                # print(s)

                if self.flag_one==True:
                    self.flag_one = False
                    total_page_num = re.search(r'"totalPageNum":(\d+),',s,re.DOTALL)
                    if total_page_num:
                        try:
                            BaiduQiye.logyyx.info("正在查看关键字key页数为：{}".format(self.start_page, ))
                            self.total_page_num = int(total_page_num.group(1))
                            # self.start_page = self.total_page_num
                        except Exception as e:
                            BaiduQiye.logyyx.info("页码转换异常{}".format(e))

                partter = re.findall(r'''<a class="zx-list-item-url".*?target="_blank".*?href=.*?title=.*?>''',s,re.DOTALL)


                if len(partter) ==0:
                    return False
                else:
                    url_list = [re.search('.*?href="(.*?)" title=.*?', x).group(1) for x in partter]
                    if url_list:
                        BaiduQiye.logyyx.info("获取列表信息成功 入队列")
                    if self.start_page < self.total_page_num:
                        self.start_page+=1
                        # url_list = self.start_list_page_url()
                        BaiduQiye.logyyx.info("正在向上翻第{}页：".format(self.start_page))
                        self.start_list_page_url(key)

                    else:
                        BaiduQiye.logyyx.info("翻页结束进行下一轮关键字爬取")
                    self.q.put(url_list)
                    # return url_list
            else:
                self.ip = ips
                BaiduQiye.logyyx.info("{}ip被封 使用代理ip:{} url:{}redirect{}".format(r.status_code,self.ip,r.url,r.headers['Location']))
                self.start_list_page_url(key)

        else:
            BaiduQiye.logyyx.info("响应失败：状态{}--请求连接：{}".format(r.status_code, r.url))

    # def grequests_detail_page(self,url_list):
    #     list_url = [grequests.get(self.domain+x, headers=self.header) for x in url_list]
    #     response_detail = grequests.map(list_url, size=1)
    #     return response_detail

    def requests_detail_page(self,url):
        response_detail = self.request_url_list(self.domain+url)
        if response_detail and response_detail.status_code==200:
            return response_detail
        else:
            self.requests_detail_page(self.domain+url)

        # try:
        #     urls = url
        #     r = requests.get(url=urls,headers=self.header,proxies = self.ips,timeout=16,allow_redirects=False)
        #     r.encoding = "utf-8"
        #     return r
        # except Exception as e:
        #     self.ips = getip()
        #     BaiduQiye.logyyx.info("请求异常{}-继续使用代理ip:{}".format(e,self.ips))
        #     # self.start_list_page_url()
        #     self.request_url_list(url)
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
        resp1 = self.request_url_list(url1)
        if resp1:
            if resp1.status_code == 200:

                dict_str = resp1.content.decode('unicode_escape').replace("\\","").replace(" ","").replace("\n","").replace("\t","")
                item = {}
                dict_type = eval(dict_str).get("data")
                print(dict_type)
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
                item["register_authority"] = ""
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
                print(item)
                return item
        else:
            global ips
            self.ip = ips
            BaiduQiye.logyyx.info("ip被封 使用代理ip:{} url:{}".format(self.ip,resp1.url))
            self.request_url_list(url1)

    @staticmethod
    def app():



        BaiduQiye.logyyx.info("程序初始化")
        baiduqiye = BaiduQiye()
        BaiduQiye.logyyx.info("程序开始启动")
        redis_connect = BaiduQiye.utils.connect_redis()
        while True:
            key = redis_connect.spop("beian")
            if key:
                BaiduQiye.logyyx.info("开始请求关键字：{}".format(key))
                baiduqiye.start_list_page_url(key)

                while not baiduqiye.q.empty():

                    url_list = baiduqiye.q.get()
                    print(url_list,3306)
                    for url in url_list:
                        response_detail = baiduqiye.requests_detail_page(url)
                        BaiduQiye.logyyx.info("返回详情页信息成功")
                        print(response_detail)
                        try:
                            pid, tk, time1 = baiduqiye.analysis_detail_paramenter(response_detail)

                            item = baiduqiye.extract_json(pid, tk, time1)
                        except Exception as e:
                            continue

                        BaiduQiye.logyyx.info("解析数据信息成功")
                        print(item)
                        if item["company_name"]:
                            BaiduQiye.utils.insertMysql(item, BaiduQiye.logyyx)

                            flag2 = BaiduQiye.utils.insertEs(item)
                            if flag2 == True:
                                BaiduQiye.logyyx.info("insert es seccess")
                            elif flag2 == False:
                                BaiduQiye.logyyx.info("insert es exist")
                            elif "插入es异常" in flag2:
                                BaiduQiye.logyyx.info(flag2)
                # baiduqiye.t1function(key,baiduqiye)
                # baiduqiye.("新网")
        # r = baiduqiye.request_url_list()
        #
        # t2 = threading.Thread(target=baiduqiye.read_q, args=(baiduqiye,))
        # t1.start()
        # t2.start()
        # t1.join()
        #
        # # BaiduQiye.logyyx.info("--------------------")
        # # BaiduQiye.logyyx.info(url_list)
        # # BaiduQiye.logyyx.info("--------------------3333")
        #
        # url_lists = []
        # if not baiduqiye.q.empty():
        #     # for i in range(baiduqiye.q.qsize()):






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








