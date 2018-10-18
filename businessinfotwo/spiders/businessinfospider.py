# -*- coding: utf-8 -*-
import scrapy


class BusinessinfospiderSpider(scrapy.Spider):
    name = 'businessinfospider'
    allowed_domains = ['71ab.com']
    start_urls = ['http://www.71ab.com']




    def parse(self, response):
        pass
