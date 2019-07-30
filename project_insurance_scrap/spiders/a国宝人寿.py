# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A国宝人寿Spider(scrapy.Spider):
    name = '国宝人寿'
    #https://www.guobaojinrong.com/PublicInfo/Index/114

    def start_requests(self):
        urls = ['https://www.guobaojinrong.com/PublicInfo/Index/114'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
            part = re.split('<td',part)
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '国宝人寿'
            item['product_type'] = shan.str_extract('9pt;">(.*?)</span>',part[2])
            item['product_name'] = shan.str_extract('9pt;">(.*?)</span>',part[3]) 
            item['product_sale_status'] = shan.str_extract('9pt;">(.*?)</span>',part[6]) 
            item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part[4]) 
                # 输出数据
            yield item
