# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A阳光人寿Spider(scrapy.Spider):
    name = '阳光人寿'
    #https://wecare.sinosig.com/common/customerservice/html/grzscp.shtml

    def start_requests(self):
        zaishou_urls = ['https://wecare.sinosig.com/common/customerservice/html/grzscp.shtml',#个险
                        'https://wecare.sinosig.com/common/customerservice/html/ttzscp.shtml'] #团险
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['https://wecare.sinosig.com/common/customerservice/html/grtscp.shtml', #个险
                         'https://wecare.sinosig.com/common/customerservice/html/tttscp.shtml'] #团险
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('#dclcot_10 span a').extract()
        result = shan.str_keep('险',result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '阳光人寿'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
                item['product_sale_status'] = '在售'
                link = shan.str_extract("http(.*)pdf",part)
                if "wecare" in link:
                    item['product_contract_link'] = "http" + link + "pdf"
                else:
                    item['product_contract_link'] = "https://wecare.sinosig.com" + shan.str_extract('href="(.*)">',part)
                # 输出数据
                yield item 
                
        next_pages = re.findall("grzscp_\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-2)]
        for next_page in next_pages:
            yield response.follow(next_page,callback=self.zaishou_parse)       
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('#dclcot_10 span a').extract()
        result = shan.str_keep('险',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '阳光人寿'
            item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http" + shan.str_extract("http(.*)pdf",part) + "pdf"
                # 输出数据
            yield item 

        next_pages = re.findall("grzscp_\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-2)]
        for next_page in next_pages:
            yield response.follow(next_page,callback=self.tingshou_parse) 