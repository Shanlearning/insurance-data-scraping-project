# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A大都会人寿Spider(scrapy.Spider):
    name = '大都会人寿'
    #https://www.metlife.com.cn4发          

    def start_requests(self):
        zaishou_urls = ['https://www.metlife.com.cn/information-disclosure/public-information-disclosure/basic-information/basic-product-information/available-products/'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['https://www.metlife.com.cn/information-disclosure/public-information-disclosure/basic-information/basic-product-information/discontinued-products/']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.width-100-authored a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '大都会人寿'
                item['product_name'] = shan.str_extract('公司(.*?)</a>',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "https://www.metlife.com.cn"+ shan.str_extract('href="(.*)zip',part) + "zip"
                # 输出数据
                yield item 
                
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.width-80-authored a').extract()
        result = shan.str_keep('险',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '大都会人寿'
            item['product_name'] = shan.str_extract('公司(.*?)</a>',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "https://www.metlife.com.cn"+ shan.str_extract('href="(.*)pdf',part) + "pdf"
            
            # 输出数据
            yield item 