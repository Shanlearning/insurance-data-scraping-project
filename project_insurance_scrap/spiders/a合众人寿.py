# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A合众人寿Spider(scrapy.Spider):
    name = '合众人寿'
    #http://www.unionlife.com.cn/unionlife/_public_basic/jbxx/cpjbxx/1000032461/index.html

    def start_requests(self):
        zaishou_urls = ['http://www.unionlife.com.cn/unionlife/_public_basic/jbxx/cpjbxx/1000032461/index.html'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.unionlife.com.cn/unionlife/_public_basic/jbxx/cpjbxx/1000030596/index.html']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result =  result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '合众人寿'
                item['product_name'] = "合众" + shan.str_extract('合众(.*?)<',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.unionlife.com.cn"+ shan.str_extract('href="(.*)" style',part)
                # 输出数据
                yield item 
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result =  result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '合众人寿'
                item['product_name'] = "合众" + shan.str_extract('合众(.*?)<',part)
                item['product_sale_status'] = '停售'
                item['product_contract_link'] = "http://www.unionlife.com.cn"+ shan.str_extract('href="(.*)" style',part)
            # 输出数据
                yield item 
