# -*- coding: utf-8 -*-
import scrapy


class A太平洋保险Spider(scrapy.Spider):
    name = '太平洋保险'
    allowed_domains = ['aaa.com']
    start_urls = ['http://aaa.com/']

    def parse(self, response):
        pass
