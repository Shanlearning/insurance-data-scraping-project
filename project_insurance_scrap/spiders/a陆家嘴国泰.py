# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A陆家嘴国泰Spider(scrapy.Spider):
    name = '陆家嘴国泰'
    #http://www.cathaylife.cn/publish/main/113/index.html
    

    def start_requests(self):
        urls = ['http://www.cathaylife.cn/publish/main/113/index.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('#a2 font , .aproName').extract()
        zs_result = result[0:shan.which(shan.str_detect("人寿保险", result))[0]]
        ts_result = result[shan.which(shan.str_detect("人寿保险", result))[0]:(shan.which(shan.str_detect("zip", result))[0]-1)]
        
        zs_result = shan.str_keep('国泰',zs_result) 
        ts_result = shan.str_keep('国泰',ts_result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '陆家嘴国泰'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = "http://www.cathaylife.cn" + shan.str_extract('href="(.*)"',part)     
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '陆家嘴国泰'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = "http://www.cathaylife.cn" + shan.str_extract('href="(.*)"',part) 
                # 输出数据
                yield item 
