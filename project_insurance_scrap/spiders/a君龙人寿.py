# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A君龙人寿Spider(scrapy.Spider):
    name = '君龙人寿'
    #http://www.kdlins.com.cn/info!detail.action

    def start_requests(self):
        urls = ['http://www.kdlins.com.cn/info!detail.action'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('君龙',result)
        result = shan.str_keep('bgcolor="#F5F2EF"',result)
        result = result[5:len(result)]   
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '君龙人寿'
            item['product_name'] = "君龙" + shan.str_extract('君龙(.*?)\r\n\t\t\t\t',part)
            item['product_sale_status'] = shan.str_extract('\t(.*?)售',part) + "售"
            item['product_contract_link'] = "http://www.kdlins.com.cn/"+ shan.str_extract('href="(.*?)" target',part) 
                # 输出数据
            yield item 
            
            
            
            
