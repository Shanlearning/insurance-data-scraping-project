# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A渤海人寿Spider(scrapy.Spider):
    name = '渤海人寿'
    #http://www.bohailife.net/xxpl/jbxx/jbxx.shtml
    

    def start_requests(self):
        urls = ['http://www.bohailife.net/xxpl/jbxx/jbxx.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract() 
        result = result[1:len(result)]
        for part in result:
            item = ProjectInsuranceScrapItem()   
            item['company_name'] = '渤海人寿'
            item['product_name'] = shan.str_extract("渤海(.*?)</p>",part)
            item['product_sale_status'] = shan.str_extract(">(\S+)售",part) + "售"
            item['product_contract_link'] = "http://www.bohailife.net"+ shan.str_extract('href="(.*?)pdf',part) +"pdf"
                # 输出数据
            yield item 
                
