#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import requests,time
ips={}
def getip():
    while True:
        try:
            pro_addr = requests.get(
        'http://dynamic.goubanjia.com/dynamic/get/6f8e9b4dcc005b5077074fea55d55f56.html?sep=3').text
            ip = pro_addr.strip()
            ips["http"] = ip
            time.sleep(4)
        except Exception as e:
            print(e, "ip接口异常")
if __name__ == "__main__":
    getip()
# ips=[]
# def buildList():
#     while True:
#         try:
#             #if IcpRecard.flags == False:
#                 #break
#             pro_addr = requests.get(
#             'http://dynamic.goubanjia.com/dynamic/get/6f8e9b4dcc005b5077074fea55d55f56.html?sep=3').text
#             ip = pro_addr.strip()
#
#             if len(ips) == 0:
#                 ips.append(ip)
#             else:
#                 ips[0] = ip
#             time.sleep(6)
#             print(ips, "22@")
#
#
#         except Exception as e:
#             print(e,"ip接口异常")