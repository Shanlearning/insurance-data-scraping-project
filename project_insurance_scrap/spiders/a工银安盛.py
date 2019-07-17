# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrapfunctions as shan

class A工银安盛Spider(scrapy.Spider):
    name = '工银安盛'
    #https://www.icbc-axa.com/public/public_base/public_base_3/publicIndex.jsp

    def start_requests(self):
        #
        urls = ['https://www.icbc-axa.com/public/public_base/public_base_3/publicIndex.jsp']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 从每一行抽取数据
        result = response.css("p , #content a , .h2_title1").extract()
        result = result[2:len(result)]
        zs_result = result[shan.which(shan.str_detect("在售", result)[0]):shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[shan.which(shan.str_detect("停售", result))[0]:shan.which(shan.str_detect("在售", result))[1]] 

        zs_result = shan.str_keep('style="color:#626263;"',zs_result) 

        ts_result = shan.str_keep('style="color:#626263;"',ts_result)
        
        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '工银安盛'
            item['product_type'] = ''

            item['product_name'] =  shan.str_extract(">(.*?)</a>",part)
            item['product_sale_status'] = '在售'

            item['product_contract_link'] = "www.icbc-axa.com"+shan.str_extract('href="(.*?)pdf',part)+"pdf"  
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item
            
        for part in ts_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '工银安盛'
            item['product_type'] = ''

            item['product_name'] =  shan.str_extract(">(.*?)</a>",part)
            item['product_sale_status'] = '停售'

            item['product_contract_link'] = "www.icbc-axa.com"+shan.str_extract('href="(.*?)pdf',part)+"pdf"  
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item