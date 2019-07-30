# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A恒大人寿Spider(scrapy.Spider):
    name = '恒大人寿'
    #http://www.lifeisgreat.com.cn/html/cpmltk/index.html

    def start_requests(self):
        urls = ['http://www.lifeisgreat.com.cn/html/cpmltk/index.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('table').extract()   
        result = re.split('售</td>',result[0])
        result = shan.str_keep('险',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '恒大人寿'
            name = shan.str_extract('>(.*?)</span>',part) 
            if "中新" in name:
                item['product_name'] = "中新" + shan.str_extract('中新(\S+)',name)
            else:
                item['product_name'] = "恒大" + shan.str_extract('恒大(\S+)',name)
            result1 = part + "售"
            item['product_sale_status'] = shan.str_extract('>(\S+)售',result1) + "售"
            item['product_contract_link'] =shan.str_extract('href="(.*?)" target',part)
            
                # 输出数据
            yield item 