# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A中法人寿Spider(scrapy.Spider):
    name = '中法人寿'
    #http://www.sfli.com.cn/cms-web/front/sinofrench/plxx/jbxx/cpjbxx/cpjbxx@1.html

    def start_requests(self):
        urls = ['http://www.sfli.com.cn/cms-web/front/sinofrench/plxx/jbxx/cpjbxx/cpjbxx@1.html'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.list-content a').extract()
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中法人寿'
            name = shan.str_extract('>·(.*?)<span>',part)
            if "目录" in name:
                item['product_name'] = name
                item['product_sale_status'] = '停售'
            elif "产品说明书" in name:
                item['product_name'] = shan.str_extract('(.*?)产品说明书',name)
                item['product_sale_status'] = '在售'
            else:
                item['product_name'] = name
                item['product_sale_status'] = '在售'
            item['product_contract_link'] = "http://www.sfli.com.cn"+ shan.str_extract('href="(.*?)" target',part) 
                # 输出数据
            yield item 

        a = response.css('option').extract()
        b = shan.str_extract('value="(.*?)">',a)
        b = b[1:len(b)]
        for part in b:
            yield response.follow("http://www.sfli.com.cn" + part, callback=self.parse)