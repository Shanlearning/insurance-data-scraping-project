# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A太保安联Spider(scrapy.Spider):
    name = '太保安联'
    #http://health.cpic.com.cn/jkx/gkxxpl/jbxx/bxcpmljtk/index.shtml

    def start_requests(self):
        urls = ['http://health.cpic.com.cn/jkx/gkxxpl/jbxx/bxcpmljtk/index.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('险',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太保安联'
            item['product_name'] = shan.str_extract('target="_blank">(.*?)</a>',part)
            item['product_sale_status'] = ''
            item['product_contract_link'] = "http://health.cpic.com.cn"+ shan.str_extract('href="(.*?)" target',part) 
                # 输出数据
            yield item 

        a = response.css('.z_num').extract()
        b = shan.str_extract('href="(.*?)">',a)
        c = shan.str_keep('index',b)
        for part in c:
            yield response.follow("http://health.cpic.com.cn/jkx/gkxxpl/jbxx/bxcpmljtk/" + part, callback=self.parse)
