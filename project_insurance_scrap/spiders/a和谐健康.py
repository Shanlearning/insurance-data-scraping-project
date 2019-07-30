# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re 

class A和谐健康Spider(scrapy.Spider):
    name = '和谐健康'
    #http://www.hexiehealth.com/gkxxpl/jbxx/zscp/index.htm

    def start_requests(self):
        urls = ['http://www.hexiehealth.com/gkxxpl/jbxx/zscp/index.htm'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = re.split("tr",response.text) 
        result = result[shan.which(shan.str_detect("在售产品目录及条款", result))[0]:shan.which(shan.str_detect("在售产品目录及条款", result))[1]]
        result = shan.str_keep('和谐',result)
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '和谐健康'
            item['product_name'] = "和谐" + shan.str_extract('和谐(.*?)</span>',part)
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "http://www.hexiehealth.com/docs"+ shan.str_extract('/docs(.*?)pdf"',part) + "pdf"
                # 输出数据
            yield item 
