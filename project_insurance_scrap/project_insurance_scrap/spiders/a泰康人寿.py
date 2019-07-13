# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem

class A泰康人寿Spider(scrapy.Spider):
    name = '泰康人寿'
    
    #http://www.taikanglife.com/publicinfonew/basicnew/pubproduct/commonprodinfo/saleproductnew/list_397_1.html
    
    def start_requests(self):
        
        zaishou_urls = ['http://www.taikanglife.com/publicinfonew/basicnew/pubproduct/commonprodinfo/saleproductnew/list_397_1.html',                        ] 
        
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.taikanglife.com/publicinfonew/basicnew/pubproduct/commonprodinfo/stopproductnew/list_398_1.html',  
                       ]
        
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback= self.tingshou_parse)
                     
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").getall()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()  
                
                part = re.findall('<a(.*)?</a>',part)
                
                item['company_name'] = '泰康人寿'            
                item['product_type'] = ''
                item['product_id'] = ''
                name = re.sub(" ","",re.findall('>.*',part[0])[0])
                name = re.sub(">","",name)
                item['product_name'] = name
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = re.findall('href="(.*)?" ',part[1])[0]
                item['product_price_link'] = ''
            
                item['product_start_date'] =  ''
                item['product_end_date'] = ''  
                # 输出数据
                yield item                  
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css("tr").getall()
        result = result[1:len(result)]
        
        for part in result:
                # 停售保险的内容输入
                item = ProjectInsuranceScrapItem()    
                
                part = re.findall('<a(.*)?</a>',part)
                item['company_name'] = '泰康人寿'
                
                item['product_type'] = ''
                item['product_id'] = ''
                name = re.sub(" ","",re.findall('>.*',part[0])[0])
                name = re.sub(">","",name)
                item['product_name'] = name
                item['product_sale_status'] = '停售'
                item['product_contract_link'] = re.findall('href="(.*)?" ',part[1])[0]
                item['product_price_link'] = ''
            
                item['product_start_date'] =  ''
                item['product_end_date'] = ''  
                # 输出数据
                yield item 
        