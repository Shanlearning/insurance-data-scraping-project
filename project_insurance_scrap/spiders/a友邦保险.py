# -*- coding: utf-8 -*-
import scrapy


class A友邦保险Spider(scrapy.Spider):
    name = '友邦保险'
    allowed_domains = ['aaa.com']
    start_urls = ['http://aaa.com/']

    def parse(self, response):
        pass
