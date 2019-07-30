# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A长生人寿Spider(scrapy.Spider):
    name = '长生人寿'
    #http://www.gwcslife.com/main/index/gkxxplzl/jbxx/cpjbxx/4806/index.html

    def start_requests(self):
        zaishou_urls = ['http://www.gwcslife.com/main/index/gkxxplzl/jbxx/cpjbxx/4806/index.html'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.gwcslife.com/main/index/gkxxplzl/jbxx/cpjbxx/4976/index.html']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result1 = response.css('tr').extract()
        result = shan.str_keep(".xl84",result1)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '长生人寿'
                name = shan.str_extract('xl84(.*?)</td>',part)
                name = shan.str_extract('">(\S+)</',name)
                if "</span>" in name:
                    item['product_name'] = shan.str_extract('\S+险',name)
                else:
                    item['product_name'] = name
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.gwcslife.com"+ shan.str_extract('href="(.*)pdf"',part)+"pdf"
                
                # 输出数据
                yield item 
                
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_drop('停售',result)
        result = shan.str_keep('险',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '长生人寿'
            name = shan.str_extract('">(.*?)</td>',part) 
            if "<" in name:
                item['product_name'] = shan.str_extract('>(.*?)<',name) 
            else:
                item['product_name'] = name
            link = shan.str_extract('href="(.*)pdf"',part)
            if "http" in link:
                item['product_contract_link'] = link + "pdf"
            else: 
                item['product_contract_link'] = "http://www.gwcslife.com"+ shan.str_extract('href="(.*)pdf"',part)+"pdf"
            item['product_sale_status'] = '停售'
            
            
            # 输出数据
            yield item 
