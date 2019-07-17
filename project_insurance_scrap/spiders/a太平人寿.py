# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A太平人寿Spider(scrapy.Spider):
    name = '太平人寿'
    #http://tppension.cntaiping.com/info-bxcp/
    
    def start_requests(self):
        
        urls = ['http://life.cntaiping.com/info-bxcp/']
        for url in urls:        
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        # 从每一行抽取数据
        
        result = response.css(".ts_product")
        zs_result = result[0].css("tr").getall()
        zs_result = shan.str_keep("条款PDF文档",zs_result)
               
        for part in zs_result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太平人寿'

            item['product_name'] = shan.str_extract('<td>(.*)</td>',part)
            item['product_sale_status'] = '在售'

            item['product_contract_link'] = shan.str_extract('href="(.*)?">',part)

                # 输出数据
            yield item
            
        ts_result =  result[1].css("tr").getall()
        ts_result = shan.str_keep("条款PDF文档", ts_result)

        for part in ts_result:
                # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太平人寿'

            item['product_name'] = shan.str_extract('<td>(.*)</td>', part)
            item['product_sale_status'] = '停售'

            item['product_contract_link'] = shan.str_extract('href="(.*)?">',part)

                # 输出数据
            yield item 
       