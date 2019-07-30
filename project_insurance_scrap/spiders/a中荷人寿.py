# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A中荷人寿Spider(scrapy.Spider):
    name = '中荷人寿'
    #http://www.bob-cardif.com/xinxipilu/jibenxinxi/gongsigaikuang/100000348849.html
    
    def start_requests(self):
        urls = ['http://www.bob-cardif.com/xinxipilu/jibenxinxi/gongsigaikuang/100000348849.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中荷人寿'
            item['product_name'] = "中荷" + shan.str_extract('中荷(.*?)</td>',part)
            item['product_sale_status'] = ''
            item['product_contract_link'] = "http://www.bob-cardif.com/_upload/products_all/products"+ shan.str_extract('/_upload/products_all/products(.*?)pdf',part) + "pdf" 
            price = shan.str_extract('/_upload/products_all/rates(.*?)pdf',part)
            if "/" in price:
                item['product_price_link'] = "http://www.bob-cardif.com/_upload/products_all/rates" + shan.str_extract('/_upload/products_all/rates(.*?)pdf',part)+"pdf"
            else:
                item['product_price_link'] = '无'
                # 输出数据
            yield item 