# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A德华安顾Spider(scrapy.Spider):
    name = '德华安顾'
    #https://www.ergo-life.cn/gkxxpl.html

    def start_requests(self):
        urls = ['https://www.ergo-life.cn/gkxxpl.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.product_right_content').extract() 
        result = result[2]
        result = re.split('<tr>',result)
        
        zs_result = result[shan.which(shan.str_detect("在售", result))[0]:(shan.which(shan.str_detect("停售", result))[0]+1)]
        ts_result = result[(shan.which(shan.str_detect("停售", result))[0]+1):len(result)]
        
        zs_result = shan.str_keep('德华',zs_result) 
        ts_result = shan.str_keep('德华',ts_result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '德华安顾'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)pdf",part) + "pdf" 
                if "rar" in part:
                    item['product_official_report_list'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)rar",part) + "rar" 
                else:
                    item['product_official_report_list'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)zip",part) + "zip" 
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '德华安顾'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part) 
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)pdf",part) + "pdf" 
                if "rar" in part:
                    item['product_official_report_list'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)rar",part) + "rar" 
                else:
                    item['product_official_report_list'] = "https://www.ergo-life.cn/dhag" + shan.str_extract("dhag(.*)zip",part) + "zip" 
                # 输出数据
                yield item 