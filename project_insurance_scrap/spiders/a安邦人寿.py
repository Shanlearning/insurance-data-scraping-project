# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A安邦人寿Spider(scrapy.Spider):
    name = '安邦人寿'
    #http://www.anbang-life.com/gkxxpl/jbxx/jydbxcpmljtk/index.htm

    def start_requests(self):
        urls = ['http://www.anbang-life.com/gkxxpl/jbxx/jydbxcpmljtk/index.htm'] 
        for url in urls:        
            yield SplashRequest(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '安邦人寿'
            item['product_name'] = "安邦" + shan.str_extract('安邦(.*?)</span>',part)
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "http://www.anbang-life.com"+ shan.str_extract('href="../../..(.*?)">',part)
                # 输出数据
            yield item 