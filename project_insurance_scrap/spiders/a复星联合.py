# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A复星联合Spider(scrapy.Spider):
    name = '复星联合'
    #http://www.fosun-uhi.com/PublicInformation/BasicInformation/ProductInformation/

    def start_requests(self):
        urls = ['http://www.fosun-uhi.com/PublicInformation/BasicInformation/ProductInformation/'] 
        for url in urls:        
            yield SplashRequest(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('p').extract()
        result = shan.str_keep('条款',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '复星联合'
            name = shan.str_extract('blank">(.*?)</a>',part)
            if "停售" in name:
                item['product_name'] = shan.str_extract('(.*?)条款',name)
                item['product_sale_status'] = '停售'
            else:
                item['product_name'] = shan.str_extract('(.*?)条款',name)
                item['product_sale_status'] = '在售'
            item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part) 
                # 输出数据
            yield item 