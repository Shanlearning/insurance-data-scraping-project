# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A北大方正Spider(scrapy.Spider):
    name = '北大方正'
    #https://www.pkufi.com/t3/50-0

    def start_requests(self):
        urls = ['https://www.pkufi.com/t3/50-0'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('rtejustify', result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '北大方正'
                item['product_name'] = shan.str_extract('\xa0(.*?)</p>',part)   
                item['product_sale_status'] = shan.str_extract('<p class="rtecenter">(.*?)售',part) + "售" 
                item['product_contract_link'] = "http://www.pkufi.com"+ shan.str_extract('href="(.*)" target',part)
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        a = response.css('.pager-item').extract()
        b = shan.str_extract('href="(.*?)" title',a) 
        for part in b:
            yield response.follow(part, callback=self.parse)
                   
