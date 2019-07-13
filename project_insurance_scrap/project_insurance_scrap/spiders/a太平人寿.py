# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem

class A太平人寿Spider(scrapy.Spider):
    name = '太平人寿'
    #http://tppension.cntaiping.com/info-bxcp/
    
    def start_requests(self):
        
        urls = ['http://life.cntaiping.com/info-bxcp/']
        for url in urls:        
            yield scrapy.Request(url=url,callback=self.parse)
            

    def parse(self, response):
        # 从每一行抽取数据
        
        result = response.css(".ts_product")
                
        zs_result =  result[0].css("tr").getall()
        zs_result = zs_result[1:len(zs_result)]
        
        zs_result1 = []
        for part in zs_result:
            if "条款PDF文档" in part:
                zs_result1.append(part)
               
        for part in zs_result1:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太平人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            product_name = re.findall('<td>(.*)</td>',part)
            if product_name != []:
                product_name = product_name[0]
            else:
                product_name = ""
            item['product_name'] = product_name
            item['product_sale_status'] = '在售'
            
            product_contract_link = re.findall('href="(.*)?">',part)
            if product_contract_link != []:
                product_contract_link = product_contract_link[0]
            else:
                product_contract_link = ""           
            item['product_contract_link'] = product_contract_link
            
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
                # 输出数据
            yield item
            
        ts_result =  result[1].css("tr").getall()
        ts_result = ts_result[1:len(ts_result)]
        
        ts_result1 = []
        for part in ts_result:
            if "条款PDF文档" in part:
                ts_result1.append(part)
                
        for part in ts_result1:
                # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太平人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            product_name = re.findall('<td>(.*)</td>',part)
            if product_name != []:
                product_name = product_name[0]
            else:
                product_name = ""
            item['product_name'] = product_name
            item['product_sale_status'] = '停售'
            
            product_contract_link = re.findall('href="(.*)?">',part)
            if product_contract_link != []:
                product_contract_link = product_contract_link[0]
            else:
                product_contract_link = ""           
            item['product_contract_link'] = product_contract_link
            
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
                # 输出数据
            yield item 
       