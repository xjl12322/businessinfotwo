# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BusinessinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    company_introduce = scrapy.Field()          #'公司简介'
    tel = scrapy.Field()                        #'电话'
    contacts_people = scrapy.Field ()             #'联系人'
    m_phone = scrapy.Field()                    #'手机'

    company_name = scrapy.Field()               #'公司名称'
    status= scrapy.Field()                      #'登记状态'
    company_type = scrapy.Field()               #'企业类型'
    establish_date = scrapy.Field()             #'成立日期'
    expire_date = scrapy.Field()                #'营业期限'
    register_money = scrapy.Field()             #'注册资本'
    register_authority = scrapy.Field()         #'登记机关'
    business_scope = scrapy.Field()             #'经营范围'
    register_address = scrapy.Field()           #'注册地址'
    legal_representative = scrapy.Field()       #'法人代表'
    register_num = scrapy.Field()               #"注 册 号"
    company_website = scrapy.Field()

    industry_id = scrapy.Field()                 #"行业id"
    area_p = scrapy.Field()                    #"地区id"
    area_s = scrapy.Field()
    area_q = scrapy.Field()
    origin_id = scrapy.Field()
    industry = scrapy.Field()


class BeianItem(scrapy.Item):


    company_name = scrapy.Field()   #'公司名称'
    company_type = scrapy.Field()   #单位性质
    website_recard_num = scrapy.Field()   #备案
    website_homepage = scrapy.Field()     #网站首页
    website_name = scrapy.Field()         #网站名称
    check_date = scrapy.Field()           #审核时间


class DomainItem(scrapy.Item):
    domain = scrapy.Field()  #域名


class BaiduqiyeItem(scrapy.Item):

    company_introduce= scrapy.Field()
    tel= scrapy.Field()
    contacts_people = scrapy.Field()
    m_phone = scrapy.Field()
    company_name = scrapy.Field()
    status = scrapy.Field()
    company_type = scrapy.Field()
    establish_date = scrapy.Field()
    expire_date = scrapy.Field()
    register_money = scrapy.Field()
    register_authority = scrapy.Field()
    business_scope = scrapy.Field()
    register_address = scrapy.Field()
    legal_representative = scrapy.Field()
    register_num = scrapy.Field()
    company_website = scrapy.Field()
    area_p = scrapy.Field()
    area_s = scrapy.Field()
    area_q = scrapy.Field()
    industry_id = scrapy.Field()
    industry = scrapy.Field()