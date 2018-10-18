#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"


from scrapy.cmdline import execute


execute("scrapy crawl 17ab".split())
# execute("scrapy crawl business_info2".split())
# execute("scrapy crawl business_info_chuangyebang".split())



# import threading,requests
# import time
# ips=[]
# class Test(object):
#     def __init__(self):
#         # threading.Thread.__init__(self)
#         self._sName = "machao"
#
#     def process(self):
#         #args是关键字参数，需要加上名字，写成args=(self,)
#         th1 = threading.Thread(target=Test.buildList, args=(self,))
#         th1.start()
#         th1.join()
#
#     def buildList(self):
#         while True:
#             print(ips, "111")
#             pro_addr = requests.get(
#                 'http://dynamic.goubanjia.com/dynamic/get/6f8e9b4dcc005b5077074fea55d55f56.html?sep=3').text
#             ip = pro_addr.strip()
#             if len(ips)==0:
#                 ips.append(ip)
#             else:
#                 ips[0] = ip
#             time.sleep(7)
#             print(ips,"22")





# execute("scrapy crawl baidu_spider".split())
# execute("scrapy crawl icp_beian".split())
# execute("scrapy crawl domian_spider".split())