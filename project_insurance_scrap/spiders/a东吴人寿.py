# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A东吴人寿Spider(scrapy.Spider):
    name = '东吴人寿'
    #http://www.soochowlife.net/eportal/ui?pageId=363297

    def start_requests(self):
        urls = ['http://www.soochowlife.net/eportal/ui?pageId=363297'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('查看条款',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '东吴人寿'
            item['product_name'] = shan.str_extract('class="tw2">(.*?)</td>',part)
            if "停用" in part:
                item['product_sale_status'] = shan.str_extract('用">(.*?)</a>',part)
            else:
                item['product_sale_status'] = shan.str_extract('售">(.*?)</a>',part)      
            item['product_contract_link'] = "http://www.soochowlife.net" + shan.str_extract('href="(.*?)" target',part)
                # 输出数据
            yield item 
