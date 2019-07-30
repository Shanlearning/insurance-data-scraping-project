# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A太平养老Spider(scrapy.Spider):
    name = '太平养老'
    #http://tppension.cntaiping.com/info-bxcp/
    

    def start_requests(self):
        urls = ['http://tppension.cntaiping.com/info-bxcp/'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result =  result[1:len(result)]
        a = shan.str_detect("健康保险", result)
        zs_result = result[0:shan.which(a)[len(shan.which(a))-1]]
        ts_result = result[shan.which(a)[len(shan.which(a))-1]:(len(result))]
        
        zs_result = shan.str_keep('太平',zs_result) 
        ts_result = shan.str_keep('太平',ts_result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '太平养老'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '太平养老'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part) 
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
