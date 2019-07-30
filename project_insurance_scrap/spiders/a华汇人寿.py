# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A华汇人寿Spider(scrapy.Spider):
    name = '华汇人寿'
    #https://www.sciclife.com/base_survey/_content/13_05/02/1367479651970_1.html

    def start_requests(self):
        urls = ['https://www.sciclife.com/base_survey/_content/13_05/02/1367479651970_1.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.release_content_detail a').extract()
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '华汇人寿'
            name = shan.str_extract('-(.*?)</a>',part)
            if "停售" in name:
                item['product_name'] = shan.str_extract('.*?险',name) 
                item['product_sale_status'] = '停售'
            else:
                item['product_name'] = name 
                item['product_sale_status'] = '在售'
            item['product_contract_link'] = "https://www.sciclife.com"+ shan.str_extract('href="(.*?)">',part)
                # 输出数据
            yield item 
