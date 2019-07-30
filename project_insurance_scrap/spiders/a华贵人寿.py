# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A华贵人寿Spider(scrapy.Spider):
    name = '华贵人寿'
    #https://www.huaguilife.cn/gkxxpl/jbxx/gsgk/index.shtml

    def start_requests(self):
        urls = ['https://www.huaguilife.cn/gkxxpl/jbxx/gsgk/index.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[3:len(result)]
        for part in result:
            part = re.split('<p>',part)
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '华贵人寿'
            name = shan.str_extract('<u>(.*?)</u>',part[1])
            if "span" in name:
                item['product_name'] = shan.str_extract('>(.*?)</span>',name)
            else:
                item['product_name'] = name
            item['product_sale_status'] = shan.str_extract('华文楷体; ">(.*?)</span>',part[2]) 
            item['product_contract_link'] = "https://www.huaguilife.cn"+ shan.str_extract('href="(.*?)" zcmsattachrela',part[1])
                # 输出数据
            yield item 
