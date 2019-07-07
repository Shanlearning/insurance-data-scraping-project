# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem


class ChinalifeSpider(scrapy.Spider):
    name = 'chinalife'
    #allowed_domains = ['http://www.e-chinalife.com/']
    
    def start_requests(self):
        # 输入在售保险的第一页网址
        zaishou_urls = [
            'http://quotes.toscrape.com/page/1/',]
        for url in zaishou_urls:
            yield scrapy.Request(url=url, callback=self.zaishou_parse)
        # 输入停售保险的第一页网址
        tingshou_urls = [
            'http://quotes.toscrape.com/page/2/',]
        for url in tingshou_urls:
            yield scrapy.Request(url=url, callback=self.tingshou_parse)
            

    def zaishou_parse(self, response):                
        # 从每一行抽取数据
        for part in response.css('div.quote'):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company'] = part.css('span.text::text').get()
            item['product'] = part.css('small.author::text').get()
            item['status'] = '在售'
            item['contract_link'] = part.css('div.tags a.tag::text').getall() 
            item['price_link'] = ''
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.zaishou_parse)
            
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        for part in response.css('div.quote'):
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company'] = part.css('span.text::text').get()
            item['product'] = part.css('small.author::text').get()
            item['status'] = '停售'
            item['contract_link'] = part.css('div.tags a.tag::text').getall()
            item['price_link'] = ''
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.tingshou_parse)
    

