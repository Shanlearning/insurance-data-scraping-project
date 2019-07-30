# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A国联人寿Spider(scrapy.Spider):
    name = '国联人寿'
    #file:///private/var/folders/tr/kmjhzl0s1195cnzf9zsrk5yh0000gn/T/tmpbq2ghofg.html

    def start_requests(self):
        urls = ['file:///private/var/folders/tr/kmjhzl0s1195cnzf9zsrk5yh0000gn/T/tmpbq2ghofg.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('li').extract()
        result = shan.str_keep('条款',result)
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '国联人寿'
            item['product_name'] = shan.str_extract('target="_blank">(.*?)</a>',part)
            item['product_sale_status'] = ''
            item['product_contract_link'] = shan.str_extract('href="(.*?)" target=',part)
                # 输出数据
            yield item 
