#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/10/22 23:07"

import hashlib
import time
import requests,json
def mad5_url(url):
    '''mad加密功能
    parmes：对每个文章url链接md5加密相同长度的指纹
    '''
    urls = "@$^&)*%"+url
    if isinstance(urls,str):  #py3里全是uncode字符集 也就是str，md5前判断 因为py3 unicode不能直接md5必须转换utf-8，相反py2则不用
        urls = urls.encode("utf-8")
    try:
        md5_url = hashlib.md5()
        md5_url.update(urls)
        return md5_url.hexdigest()
    except Exception as e:
        print(e,"md5")
        return ""



def mad5_singn(urls):

    if isinstance(urls,str):
        urls = urls.encode("utf-8")
    md5_url = hashlib.md5()
    md5_url.update(urls)
    md5_url.hexdigest()
    # print(md5_url.hexdigest())
    return md5_url.hexdigest()
def getsecret_pythontool():
    innerApp = "pythontool"
    secret = "a6d903a2-dac5-4d9d-9e6b-e32caad1dafc"
    ts = str(int(time.time() * 1000))
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_singn(sign)
    return singn, innerApp, ts


def c_company(company):

    sign, innerApp, ts = getsecret_pythontool()
    response_tdk = requests.post(
        url="https://esservice.xinnet.com/rest/whois/addOrUpdateCompany?innerApp={}&ts={}&sign={}".format(innerApp, ts,sign),json=company)
    response_tdk = json.loads(response_tdk.text)

    return response_tdk["result"]




