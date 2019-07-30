# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A人保人寿Spider(scrapy.Spider):
    name = '人保人寿'
    #http://www.picclife.com/IndividualLongrisk/index_1.jhtml

    def start_requests(self):
        zaishou_urls = ['http://www.picclife.com/IndividualLongrisk/index_1.jhtml'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.picclife.com/ytscptk/index.jhtml']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('#jigou_right_k a').extract()
        result = shan.str_keep('条款',result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '人保人寿'
                item['product_name'] = shan.str_extract('>(.*?)条款',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.picclife.com"+ shan.str_extract('href="(.*)" title',part)
                # 输出数据
                yield item 
                
        a = response.css('.yeshu_icon').extract()
        b = shan.str_extract("\'(.*?)\'",a)
        for part in b:
            yield response.follow("http://www.picclife.com/IndividualLongrisk/" + part, callback=self.zaishou_parse)       
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('#jigou_right_k a').extract()
        result = shan.str_keep('条款',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '人保人寿'
            item['product_name'] = shan.str_extract('>(.*?)条款',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://www.picclife.com"+ shan.str_extract('href="(.*)" title',part)
            
            # 输出数据
            yield item 

        a = response.css('.yeshu_icon').extract()
        b = shan.str_extract("\'(.*?)\'",a)
        for part in b:
            yield response.follow("http://www.picclife.com/ytscptk/" + part, callback=self.tingshou_parse)       
                   