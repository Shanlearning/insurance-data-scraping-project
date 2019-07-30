# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A中宏人寿Spider(scrapy.Spider):
    name = '中宏人寿'
    #https://www.manulife-sinochem.com/zh-CN/public-information/basic/product

    def start_requests(self):
        #
        urls = ['https://www.manulife-sinochem.com/zh-CN/public-information/basic/product']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 从每一行抽取数据
        result = response.css(".faq-container-list").extract()
        zs_result = shan.str_keep("在售", result)
        ts_result = shan.str_keep("停售", result)
        zs_result1 = []
        for part in zs_result:
            zs_result1.extend(re.split('div class="item"', part))
        zs_result = shan.str_keep("(寿|保)险", zs_result1)

        ts_result1 = []
        for part in ts_result:
            ts_result1.extend(re.split('div class="item"', part))
        ts_result = shan.str_keep("(寿|保)",ts_result1)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '中宏人寿'
            item['product_name'] =  shan.str_extract("中宏.*?险",part)
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "www.manulife-sinochem.com"+shan.str_extract('<a href="(.*)target',part)
            # 输出数据
            yield item

        for part in ts_result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '中宏人寿'
            item['product_name'] =  shan.str_extract("中宏.*?险",part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "www.manulife-sinochem.com"+shan.str_extract('<a href="(.*)target',part)
            # 输出数据
            yield item



