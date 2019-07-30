# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A百年人寿Spider(scrapy.Spider):
    name = '百年人寿'
    #http://www.aeonlife.com.cn/info/base/cpjbxx/product/index.shtml

    def start_requests(self):
        urls = ['http://www.aeonlife.com.cn/info/base/cpjbxx/product/index.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('#list-box a').extract()
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '百年人寿'
            name = shan.str_extract('、(.*?)<em></em></a>',part)
            if "（停售）" in name:
                item['product_name'] = shan.str_extract('(.*?)（停售）',name)
                item['product_sale_status'] = '停售'
            elif "(停售)" in name:
                item['product_name'] = shan.str_extract('(.*?)停售',name)
                item['product_sale_status'] = '停售'
            else:
                item['product_name'] = name
                item['product_sale_status'] = '在售'
            item['product_contract_link'] = shan.str_extract('href="(.*?)" target',part)
                # 输出数据
            yield item 
