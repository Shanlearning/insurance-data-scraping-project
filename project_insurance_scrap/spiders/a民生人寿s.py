# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A民生人寿Spider(scrapy.Spider):
    name = '民生人寿'
    #http://www.minshenglife.com/publicinfo/productitem/1/0’
    
    def start_requests(self):
        zaishou_urls = ['http://www.minshenglife.com/publicinfo/productitem/1/0',  #个险
                       'http://www.minshenglife.com/publicinfo/productitem/1/1',  #团险
                       ] 
        for url in zaishou_urls:        
                    yield SplashRequest(url=url, callback=self.zaishou_parse)
        tingshou_urls = ['http://www.minshenglife.com/publicinfo/productitem/0/0',   #个险
                        'http://www.minshenglife.com/publicinfo/productitem/0/1',   #团险
                       ]
        for url in tingshou_urls:       
                   yield SplashRequest(url=url, callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css(".pi-pubinfo") 
        result1 = result.css("li").extract()
        for part in result1:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '民生人寿'
                a = shan.str_keep('class="pi-pls-prodname off-float-left"',part)
                item['product_type'] = ''
                item['product_id'] = ''
                item['product_name'] = shan.str_extract('>(.*?)<',a)
                item['product_sale_status'] = '在售'
                b = shan.str_keep('class="dsm-choise-zoon dsm-none"',part)
                item['product_contract_link'] = "http://www.minshenglife.com"+shan.str_extract('href="(.*?)">',b)
                item['product_price_link'] = ''
            
                item['product_start_date'] =  ''
                item['product_end_date'] = ''  
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]shtml",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.zaishou_parse)
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css(".pi-pubinfo") 
        result1 = result.css("li").extract()
        for part in result1:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '民生人寿'
            a = shan.str_keep('class="pi-pls-prodname off-float-left"',part)
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = shan.str_extract('>(.*?)<',a)
            item['product_sale_status'] = '停售'
            b = shan.str_keep('class="dsm-choise-zoon dsm-none"',part)
            item['product_contract_link'] = "http://www.minshenglife.com"+shan.str_extract('href="(.*?)">',b)
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
            # 输出数据
            yield item 
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]shtml",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.tingshou_parse)
