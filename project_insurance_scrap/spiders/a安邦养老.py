# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A安邦养老Spider(scrapy.Spider):
    name = '安邦养老'
    #http://www.anbangannuity.com/gkxxpl/jbxx/jbxxzscp/index.htm

    def start_requests(self):
        urls = ['http://www.anbangannuity.com/gkxxpl/jbxx/jbxxzscp/index.htm'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '安邦养老'
            item['product_name'] = shan.str_extract('<td>(.*?)</td>',part)
            status = shan.str_extract('>(.*?)/span>',part)
            if "#ff0000" in status:
                item['product_sale_status'] = shan.str_extract('#ff0000">(.*?)<',status)
            else:
                item['product_sale_status'] = shan.str_extract('#0000ff">(.*?)<',status)
            item['product_contract_link'] = "http://www.anbangannuity.com"+ shan.str_extract('href="../../..(.*?)">安邦养老',part) 
                # 输出数据
            yield item 