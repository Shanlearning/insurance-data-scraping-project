# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import re

class A中国人寿Spider(scrapy.Spider):
    # 抓取机名字
    name = '中国人寿'
    
    def start_requests(self):
        # 输入在售保险的第一页网址
        zaishou_urls = [
            'http://www.e-chinalife.com/help-center/xiazaizhuanqu/zaishoubaoxianchanpin.htm/',]
        for url in zaishou_urls:
            yield scrapy.Request(url=url, callback=self.zaishou_parse)
        # 输入停售保险的第一页网址
        tingshou_urls = [
            'http://www.e-chinalife.com/help-center/xiazaizhuanqu/tingbanbaoxianchanpin.html/',]
        for url in tingshou_urls:
            yield scrapy.Request(url=url, callback=self.tingshou_parse)
            
    def zaishou_parse(self, response):                
        # 从每一行抽取数据
        for part in response.css('.downlist li'):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中国人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = re.sub(" ","",re.sub("\d+[.]", "" ,part.css("a::text").getall()[1]))
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "http://www.e-chinalife.com/" + part.css("::attr(href)").get()
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('.page_down::attr(onclick)').get()
        if next_page is not None:
            next_page = 'http://www.e-chinalife.com/help-center/xiazaizhuanqu/zaishoubaoxianchanpin.htm&curtPage=' \
            + str(re.findall("\d+",next_page)[0])
            yield scrapy.Request(next_page, callback=self.zaishou_parse)
            
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        for part in response.css('.downlist li'):
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中国人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = re.sub(" ","",re.sub("\d+[.]", "" ,part.css("a::text").getall()[1]))
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://www.e-chinalife.com/" + part.css("::attr(href)").get()
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('.page_down::attr(onclick)').get()
        if next_page is not None:
            next_page = 'http://www.e-chinalife.com/help-center/xiazaizhuanqu/tingbanbaoxianchanpin.html&curtPage=' \
            +str(re.findall("\d+",next_page)[0])
            yield scrapy.Request(next_page, callback=self.tingshou_parse)
    

