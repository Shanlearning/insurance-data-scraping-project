# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A中融人寿Spider(scrapy.Spider):
    name = '中融人寿'
    #http://www.zhongronglife.com/html/pcgkcpxx/index.html

    def start_requests(self):
        urls = ['http://www.zhongronglife.com/html/pcgkcpxx/index.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        zs_result = result[shan.which(shan.str_detect("在售", result))[0]:shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[shan.which(shan.str_detect("停售", result))[0]:len(result)]
        
        zs_result = shan.str_keep('中融',zs_result) 
        ts_result = shan.str_keep('中融',ts_result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中融人寿'
                item['product_name'] = '中融' + shan.str_extract('中融(.*?)</td>',part)  
                item['product_sale_status'] = "在售" 
                part1 = re.split('</td>',part)
                if len(part1)==7:
                    item['product_official_report_list'] = shan.str_extract('href="(.*?)" target',part1[1]) 
                    item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part1[2])  
                    item['product_chief_actuary_claim_link'] = shan.str_extract('href="(.*?)" target',part1[4])  
                    item['prodcct_law_response_link'] = shan.str_extract('href="(.*?)" target',part1[5]) 
                if len(part1)==6:
                    item['product_official_report_list'] = shan.str_extract('href="(.*?)" target',part1[1]) 
                    item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part1[2])  
                    item['product_chief_actuary_claim_link'] = shan.str_extract('href="(.*?)" target',part1[3])  
                    item['prodcct_law_response_link'] = shan.str_extract('href="(.*?)" target',part1[4]) 
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中融人寿'
                item['product_name'] = '中融' + shan.str_extract('中融(.*?)</td>',part)  
                item['product_sale_status'] = "停售" 
                part1 = re.split('</td>',part)
                if len(part1)==7:
                    item['product_official_report_list'] = shan.str_extract('href="(.*?)" target',part1[1]) 
                    item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part1[2])  
                    item['product_chief_actuary_claim_link'] = shan.str_extract('href="(.*?)" target',part1[4])  
                    item['prodcct_law_response_link'] = shan.str_extract('href="(.*?)" target',part1[5]) 
                if len(part1)==6:
                    item['product_official_report_list'] = shan.str_extract('href="(.*?)" target',part1[1]) 
                    item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part1[2])  
                    item['product_chief_actuary_claim_link'] = shan.str_extract('href="(.*?)" target',part1[3])  
                    item['prodcct_law_response_link'] = shan.str_extract('href="(.*?)" target',part1[4]) 
                # 输出数据
                yield item 
