# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A瑞泰人寿Spider(scrapy.Spider):
    name = '瑞泰人寿'
   #http://www.oldmutual-guodian.com/common/onlineService/download/prosuctClause/
    
    def start_requests(self):
        urls = ['http://www.oldmutual-guodian.com/common/onlineService/download/prosuctClause/'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('#toc_total a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '瑞泰人寿'
                name = shan.str_extract('>(.*?)</a>',part) 
                if "合同" in name:
                    item['product_name'] = shan.str_extract('(\S+)合同条款',name)  
                else:
                    item['product_name'] = shan.str_extract('(\S+)条款',name)
                if "停售" in name:
                    item['product_sale_status'] = "停售"
                else:
                    item['product_sale_status'] = "在售"
                item['product_contract_link'] = "http://www.oldmutual-guodian.com/common/onlineService/download/prosuctClause/"+ shan.str_extract('href="(.*)" target',part)
                # 输出数据
                yield item 
                
