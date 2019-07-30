# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re


class A中意人寿Spider(scrapy.Spider):
    name = '中意人寿'
    #http://www.generalichina.com/jycp/

    def start_requests(self):
        zaishou_urls = ['http://www.generalichina.com/zsgxnew/'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.generalichina.com/ts/']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.list_name_text , .list_main_title').extract()
        result =  result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中意人寿'
                item['product_name'] = shan.str_extract('中.*?\ ',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.generalichina.com"+ shan.str_extract('href="(.*)pdf',part)+"pdf"
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]html",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.zaishou_parse)
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.list_name_text , .list_main_title').extract()
        result =  result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中意人寿'
            item['product_name'] = shan.str_extract('中.*?\ ',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://www.generalichina.com"+ shan.str_extract('href="(.*)pdf',part)+"pdf"
            # 输出数据
            yield item 
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]html",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.tingshou_parse)
