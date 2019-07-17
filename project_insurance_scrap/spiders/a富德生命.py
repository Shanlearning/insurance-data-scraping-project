# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A富德生命Spider(scrapy.Spider):
    name = '富德生命'
    #http://www.sino-life.com/publicinfo/jbxx/cpjbxx/jycp/
    
    def start_requests(self):
        # 输入停售保险的第一页网址
        urls = ['http://www.sino-life.com/publicinfo/jbxx/cpjbxx/jycp/']
        for url in urls:
             yield SplashRequest(url=url, callback=self.parse)
             
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").extract()
        zs_result = shan.str_keep('class="STYLE14"',result)
        ts_result = shan.str_keep('class="STYLE15"',result)
        
        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)
            item['company_name'] = '富德生命'
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = part[1]
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "https://www.sino-life.com" + shan.str_keep('upload',shan.str_extract('href="(.*)pdf',part[4])) + "pdf"
            item['product_price_link'] = ''

            item['product_start_date'] = part[2]
            item['product_end_date'] = ''
            # 输出数据
            yield item

        for part in ts_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)
            item['company_name'] = '富德生命'
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = part[1]
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "https://www.sino-life.com" + shan.str_keep('upload',shan.str_extract('href="(.*)pdf',part[4])) + "pdf"
            item['product_price_link'] = ''

            item['product_start_date'] = part[2]
            item['product_end_date'] = ''
            # 输出数据
            yield item
