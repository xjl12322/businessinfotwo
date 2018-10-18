# # -*- coding: utf-8 -*-
import scrapy
import time,re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.utils.response import response_status_message

from urllib import parse as parseurl
from ..items import BusinessinfoItem

#
class BusinessInfoChuangyebangSpider(scrapy.Spider):
    name = 'business_info_chuangyebang'
    allowed_domains = ['cyzone.cn']
    start_urls = [None]
    custom_settings = {'DOWNLOAD_DELAY': 3, 'CONCURRENT_REQUESTS_PER_IP': 3}
    "'DOWNLOAD_DELAY': 3, "



    def start_requests(self):
        start_urls = 'http://www.cyzone.cn/company/list-0-0-1-0-0/0'

        yield scrapy.Request(url=start_urls,callback=self.parse,errback=self.errback_httpbin,dont_filter=True)

    def errback_httpbin(self, failure):

        print(repr(failure))

        if failure.check(HttpError):

            response = failure.value.response
            print("httperror:{}".format(response.url))
            # self.logger.error('HttpError on %s', response.url)
            yield scrapy.Request(url=response.url, callback=self.parse, errback=self.errback_httpbin)
        elif failure.check(DNSLookupError):

            request = failure.request
            print("DNSLookupError:{}".format(request.url))
            # self.logger.error('DNSLookupError on %s', request.url)
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            print("TimeoutError on:{}".format(request.url))
            # self.logger.error('TimeoutError on %s', request.url)
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)
        else:
            request = failure.request
            print("qita:{}".format(response_status_message))
            yield scrapy.Request(url=request.url, callback=self.parse, errback=self.errback_httpbin)


    def parse(self, response):
        print("响应连接：{}".format(response.url))
        url_node_list = response.xpath('//tr[@class="table-plate item"]/td[@class="table-company-tit"]/a/@href').extract()

        for company_homepage_url in url_node_list:

            yield scrapy.Request(url="http:"+company_homepage_url,callback=self.parse_homepage,errback=self.errback_httpbin)
        page_num = response.xpath('//div[@id="pages"]/span/text()').extract_first()
        next_page = response.xpath('//div[@id="pages"]//a[contains(text(),"下一页")]/@href').extract_first()
        print(next_page,"xpath")
        next_page_url = parseurl.urljoin(response.url,next_page)
        partter = re.search(".*?-0-0-(\d+)-0-0/0", next_page_url).group(1)
        if int(page_num)!=partter:
            print("请求下一页:{}".format(next_page_url))
            yield scrapy.Request(url=next_page_url,callback=self.parse,errback=self.errback_httpbin,dont_filter=True)
        else:
            pass
#
    def parse_homepage(self,response):

        print("详情信息页：{}".format(response.url))
        company_name = response.xpath('//li[@class="time"]/text()').extract_first(default="").replace("公司全称：", "")
        if company_name == "" or company_name == None or "公司" not in company_name:
            pass
        else:
            company_website = response.xpath('//div[contains(text(),"公司官网")]/a/text()').extract_first(default="")

            company_introduce = response.xpath('string(//div[@class="info-box"])').extract_first(default="").strip()
            company_introduce = company_introduce.replace("  ","").replace("\n","")
            business_scope_list =response.xpath('//i[contains(@class,"i6")]/following-sibling::span/a/text()').extract()
            if business_scope_list:
                business_scope = ",".join(business_scope_list)
                print(business_scope,"333333")
            else:
                business_scope = ""
            register_num = response.xpath('//div[@class="qcc"]/p/span[contains(text(),"注册号")]/../text()').extract_first(
                default="")
            status = response.xpath('//div[@class="qcc"]/p/span[contains(text(),"经营状态")]/../text()').extract_first(default="")

            company_type = response.xpath(
                '//div[@class="qcc"]/p/span[contains(text(),"公司类型")]/../text()').extract_first(default="")
            establish_date = response.xpath(
                '//div[@class="qcc"]/p/span[contains(text(),"成立日期")]/../text()').extract_first(default="")
            if establish_date != "":
                timeArray = time.strptime(establish_date, "%Y-%m-%d")
                establish_date = time.strftime('%Y{y}%m{m}%d{d}', timeArray).format(y='年', m='月', d='日')
            register_address = response.xpath(
                '//div[@class="qcc"]/p/span[contains(text(),"住所")]/../text()').extract_first(default="")
            legal_representative = response.xpath(
                '//div[@class="qcc"]/p/span[contains(text(),"法定代表")]/../text()').extract_first(default="")
            register_money = response.xpath('//div[@class="qcc"]/p/span[contains(text(),"注册资本")]/../text()').extract_first(default="")
            origin_id = 2

            item = BusinessinfoItem()
            item["company_website"] = company_website
            item["company_introduce"] = company_introduce
            item["tel"] = ""
            item["contacts_people"] = ""
            item["m_phone"] = ""
            item["company_name"] = company_name
            item["status"] = status
            item["company_type"] = company_type
            item["establish_date"] = establish_date
            item["expire_date"] = ""
            item["industry_id"] = ""
            item["register_money"] = register_money
            item["register_authority"] = ""
            item["business_scope"] = business_scope
            item["register_address"] = register_address
            item["legal_representative"] = legal_representative
            item["register_num"] = register_num
            item["origin_id"] = origin_id
            item["area_p"] = None
            item["area_s"] = None
            item["area_q"] = None
            item["industry_id"] = None
            item["industry"] = None
            yield item




