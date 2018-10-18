# -*- coding: utf-8 -*-
import scrapy
import time,re,redis

from urllib import parse as parseurl
from ..items import BusinessinfoItem
from scrapy.exceptions import CloseSpider
from ..settings import *
from ..utils_common.bloomfilter2 import BloomFilter
class BusinessInfoSpider2(scrapy.Spider):
    name = '17ab'
    allowed_domains = ['71ab.com']
    start_urls = [None]
    custom_settings = {'DOWNLOAD_DELAY': 2,"CONCURRENT_REQUESTS":3}
    bf = BloomFilter()
    # def __init__(self):
    #     self.pool = redis.ConnectionPool(host=REDISDB[CONRENT_CONF]["REDIS_HOST"], port=REDISDB[CONRENT_CONF]["REDIS_PORT"], db=REDISDB[CONRENT_CONF]["REDIS_DB"])
    #     self.r = redis.Redis(connection_pool=self.pool)


    def start_requests(self):

        headers = {
            "Referer": "http://www.71ab.com",
            "Upgrade-Insecure-Requests": "1"
            }
        yield scrapy.Request(url='http://www.71ab.com/Province_0.html',headers=headers,callback=self.parse)


    def parse(self, response):
        print(response.status)
        print(len(response.text))
        href_list = response.xpath('//a[@class="la13"]/@href').extract()
        for x in href_list:
            url = parseurl.urljoin(response.url,x)
            if self.bf.isContains(url):  # 判断字符串是否存在
                print('url exists!')
            else:
                print('url not exists!')
                print("请求详情信息页：{}".format(url))
                self.bf.insert('http://www.sina.com.cn/')
            yield scrapy.Request(url=url,callback=self.parse_item)
        page_node = response.xpath('//div/a[contains(text(),"下一页")]/@href').extract_first(default=" ")
        print(page_node,"2222")
        if len(page_node)>3:
            page_next = parseurl.urljoin(response.url,page_node)
            print("开始请求下一页：{}".format(page_next))
            yield scrapy.Request(url=page_next, callback=self.parse)


    def parse_item(self,response):
        print("响应详情信息页：{}".format(response.url))
        print(len(response.text),"2")
        company_name = response.xpath(
            '//th[contains(text(),"名称")]//following-sibling::a[@id="Label1"]/text()').extract_first(default=None)

        if company_name ==None:
            pass
        else:
            area_q = ""
            area_p = response.xpath('//a[@id="HyperLink1"]/@href').extract_first()
            area_p = re.search('Province_(\d+).*?html',area_p,re.S)
            if area_p==None:
                area_p=""
                area_s = ""
            else:
                area_p = area_p.group(1)
                area_s = response.xpath('//a[@id="HyperLink2"]/@href').extract_first()

                area_s = re.search(r'Province_{}_(\d+).*?html'.format(area_p), area_s,re.I)
                if area_s != None:
                    area_s = area_s.group(1)

            company_introduce = response.xpath('//span[@id="marq"]/text()').extract_first(default="")
            company_introduce = company_introduce.replace("  ","").replace("\n","")
            email = response.xpath(
                '//td[contains(text(),"邮件")]//following-sibling::span[@id="Label7"]/text()').extract_first()
            contacts_people = response.xpath(
                '//td[contains(text(),"联系")]//following-sibling::span[@id="Label2"]/text()').extract_first()
            m_phone = response.xpath(
                '//td[contains(text(),"电话")]//following-sibling::span[@id="Label4"]/text()').extract_first()


            establish_str= response.xpath('//td[contains(text(),"注册")]//following-sibling::span[@id="Label5"]/text()').extract_first().strip()
            timeArray = time.strptime(establish_str, "%Y/%m/%d")
            establish_date = time.strftime('%Y{y}%m{m}%d{d}',timeArray).format(y='年', m='月', d='日')


            register_address = response.xpath('//td[contains(text(),"地址")]//following-sibling::span[@id="Label3"]/text()').extract_first(default="")
            industry = response.xpath('//td[contains(text(),"行业")]//following-sibling::span[@id="Label10"]/text()').extract_first(default="")


            company_website = response.xpath('//td[contains(text(),"网址")]//following-sibling::a[@id="Label8"]/text()').extract_first(default="")
            print("11111111111111111111111111111")
            print(company_name)
            print("22222222222222222222222222222")
            origin_id = 2
            item = BusinessinfoItem()
            item["company_website"] = company_website
            item["company_introduce"] = company_introduce
            item["tel"] = ""
            item["contacts_people"] = contacts_people
            item["m_phone"] = m_phone
            item["company_name"] = company_name
            item["status"] = ""
            item["company_type"] = ""
            item["establish_date"] = establish_date
            item["expire_date"] = ""
            item["industry_id"] = ""
            item["register_money"] = ""
            item["register_authority"] = ""
            item["business_scope"] = ""
            item["register_address"] = register_address
            item["legal_representative"] = ""
            item["register_num"] = ""
            item["origin_id"] = origin_id
            item["area_p"] = area_p
            item["area_s"] = area_s
            item["area_q"] = None
            item["industry_id"] = None
            item["industry"] = industry
            yield item

