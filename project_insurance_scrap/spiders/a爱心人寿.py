# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A爱心人寿Spider(scrapy.Spider):
    name = '爱心人寿'
    #http://www.aixin-ins.com/cpjbxx/372.jhtml

    def start_requests(self):
        urls = ['http://www.aixin-ins.com/cpjbxx/372.jhtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('爱心',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '爱心人寿'
            item['product_name'] = shan.str_extract('>(.*?)</a>',part)
            item['product_sale_status'] = shan.str_extract('\n(.*?)售',part) + "售"
            item['product_contract_link'] = "http://www.aixin-ins.com"+ shan.str_extract('href="(.*?)pdf',part) + "pdf"
                # 输出数据
            yield item
