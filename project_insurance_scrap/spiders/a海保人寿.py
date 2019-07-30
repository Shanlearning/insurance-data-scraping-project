# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A海保人寿Spider(scrapy.Spider):
    name = '海保人寿'
    #https://www.haibao-life.com/gkxxpl/cpjbxx/zscp/

    def start_requests(self):
        zaishou_urls = ['https://www.haibao-life.com/gkxxpl/cpjbxx/zscp/'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['https://www.haibao-life.com/gkxxpl/cpjbxx/tscp/index.shtml#chooseBtn']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.article_content_ul').extract()
        result = re.split('<ul>',result[0])
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '海保人寿'
                item['product_name'] = shan.str_extract('海.*?险',part) 
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = shan.str_extract('href="(.*)">',part)
                # 输出数据
                yield item 
                
        next_pages = re.findall("index_\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-1)]
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.zaishou_parse)
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.article_content_ul').extract()
        result = re.split('<ul>',result[0])
        result = result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '海保人寿'
            item['product_name'] = shan.str_extract('海.*?险',part) 
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = shan.str_extract('href="(.*)">',part)
            
            # 输出数据
            yield item 

        next_pages = re.findall("index_\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-1)]
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.tingshou_parse)    
                   