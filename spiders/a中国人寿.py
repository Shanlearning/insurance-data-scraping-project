# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import re

class ChinalifeSpider(scrapy.Spider):
    # 抓取机名字
    name = '中国人寿'
    
    # 抓取的网页套路
    zaishou_url_begin = 'http://www.e-chinalife.com/help-center/xiazaizhuanqu/zaishoubaoxianchanpin.htm&curtPage='
    zaishou_url_end = ''
    tingshou_url_begin = 'http://www.e-chinalife.com/help-center/xiazaizhuanqu/tingbanbaoxianchanpin.html&curtPage='
    tingshou_url_end = ''
    
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
            

    def zaishou_parse(self, response,cn_name=name,next_url_begin = zaishou_url_begin,
                      next_url_end = zaishou_url_end):                
        # 从每一行抽取数据
        for part in response.css('.downlist li'):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company'] = cn_name
            item['product'] = part.css("a::text").getall()[1],
            item['status'] = '在售'
            item['contract_link'] = "http://www.e-chinalife.com/" + part.css("::attr(href)").get()
            item['price_link'] = ''
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('.page_down::attr(onclick)').get()
        if next_page is not None:
            next_page = next_url_begin+str(re.findall("\d+",next_page)[0])+next_url_end
            yield scrapy.Request(next_page, callback=self.zaishou_parse)
            
    def tingshou_parse(self, response,cn_name=name,next_url_begin = tingshou_url_begin , 
                       next_url_end = tingshou_url_end):                
        # 从每一行抽取数据
        for part in response.css('.downlist li'):
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company'] = cn_name
            item['product'] = part.css("a::text").getall()[1],
            item['status'] = '停售'
            item['contract_link'] = "http://www.e-chinalife.com/" + part.css("::attr(href)").get()
            item['price_link'] = ''
            # 输出数据
            yield item 
        
        # 找到下一页的代码
        next_page = response.css('.page_down::attr(onclick)').get()
        if next_page is not None:
            next_page = next_url_begin+str(re.findall("\d+",next_page)[0])+next_url_end
            yield scrapy.Request(next_page, callback=self.tingshou_parse)
    

