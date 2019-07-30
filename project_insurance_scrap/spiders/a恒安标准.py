# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A恒安标准Spider(scrapy.Spider):
    name = '恒安标准'
    #http://www.hengansl.com/cha/169455.html

    def start_requests(self):
        urls = ['http://www.hengansl.com/cha/2304450.html', #个人保险
                'http://www.hengansl.com/cha/2304451.html', #团体保险
                'http://www.hengansl.com/cha/49308255.html', #网销保险
                'http://www.hengansl.com/cha/2304452.html', #银行保险
                'http://www.hengansl.com/cha/2304453.html']  #多元保险
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.list_ul a , .list_title').extract()
        zs_result = result[(shan.which(shan.str_detect("在售", result))[0]+1):shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[(shan.which(shan.str_detect("停售", result))[0]+1):len(result)]
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '恒安标准'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = shan.str_extract('href="(.*)" target=',part)     
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '恒安标准'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = shan.str_extract('href="(.*)" target=',part) 
                # 输出数据
                yield item 
