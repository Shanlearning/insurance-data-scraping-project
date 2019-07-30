# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A人保健康Spider(scrapy.Spider):
    name = '人保健康'
    #http://www.picchealth.com/tabid/2318/Default.aspx

    def start_requests(self):
        zaishou_urls = ['http://www.picchealth.com/tabid/2318/Default.aspx'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.picchealth.com/tabid/2319/Default.aspx']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('#ess_contentpane a').extract()
        result =  result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '人保健康'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.picchealth.com"+ shan.str_extract('href="(.*)" id',part)
                # 输出数据
                yield item 
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('#ess_contentpane a').extract()
        result =  result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '人保健康'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part)
                item['product_sale_status'] = '停售'
                item['product_contract_link'] = "http://www.picchealth.com"+ shan.str_extract('href="(.*)" id',part)
            # 输出数据
                yield item 
