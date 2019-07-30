# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A信美相互Spider(scrapy.Spider):
    name = '信美相互'
    #https://www.trustlife.com/cms/html/productClauseSale/

    def start_requests(self):
        zaishou_urls = ['https://www.trustlife.com/cms/html/productClauseSale/'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['https://www.trustlife.com/cms/html/productClauseStop/']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('p').extract()
        result = shan.str_keep('信美',result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '信美相互'
                item['product_name'] = shan.str_extract('\r\n\t\t\t\t\t\t\t\t\t\t\t(.*?)\r\n\t\t\t\t\t\t\t\t\t\t\t</span>',part) 
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = shan.str_extract('href="(.*)" target',part)
                # 输出数据
                yield item 
                
        a = response.css('button').extract()
        b = shan.str_extract('value="(.*?)" onclick',a)
        b = b[2:(len(b)-1)]
        for part in b:
            yield response.follow("https://www.trustlife.com/cms/html/productClauseSale/index_" + part +".html", callback=self.zaishou_parse)       
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('p').extract()
        result = shan.str_keep('信美',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '信美相互'
            item['product_name'] = shan.str_extract('\r\n\t\t\t\t\t\t\t\t\t\t\t(.*?)\r\n\t\t\t\t\t\t\t\t\t\t\t</span>',part) 
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = shan.str_extract('href="(.*)" target',part)
            
            # 输出数据
            yield item 

        a = response.css('button').extract()
        b = shan.str_extract('value="(.*?)" onclick',a)
        b = b[2:(len(b)-1)]
        for part in b:
            yield response.follow("https://www.trustlife.com/cms/html/productClauseStop/index_" + part +".html", callback=self.tingshou_parse)          
                   