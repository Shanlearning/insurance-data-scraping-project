# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A北京人寿Spider(scrapy.Spider):
    name = '北京人寿'
    #https://www.beijinglife.com.cn/c/2019-04-18/485217.html

    def start_requests(self):
        urls = ['https://www.beijinglife.com.cn/c/2019-04-18/485217.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '北京人寿'
            item['product_name'] = "北京" + shan.str_extract('北京(.*?)</',part)
            item['product_sale_status'] = ''
            item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part)
                # 输出数据
            yield item