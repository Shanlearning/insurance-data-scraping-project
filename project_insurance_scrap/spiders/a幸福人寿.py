# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A幸福人寿Spider(scrapy.Spider):
    name = '幸福人寿'
    #http://www.happyinsurance.com.cn/Info/269869

    def start_requests(self):
        urls = ['http://www.happyinsurance.com.cn/Info/269869'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('P').extract()
        
        zs_result = result[shan.which(shan.str_detect("表一", result))[0]:shan.which(shan.str_detect("表二", result))[0]]
        ts_result = result[shan.which(shan.str_detect("表三", result))[0]:len(result)]
        
        zs_result = shan.str_keep('险',zs_result)
        ts_result = shan.str_keep('险',ts_result)
        
        zs_result = zs_result[1:len(zs_result)]
        ts_result = ts_result[1:len(ts_result)]
        
        for part in zs_result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '幸福人寿'
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = shan.str_extract('href="(.*?)">',part)
            name = shan.str_extract('幸福(.*?)</a>',part)
            if "（<" in name:
                item['product_name'] = "幸福" + shan.str_extract('）(.*?)</font>',name)
            else:
                item['product_name'] = "幸福" + name
            
                # 输出数据
            yield item 
            
            
        for part in ts_result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '幸福人寿'
            item['product_name'] = "幸福" + shan.str_extract('幸福(.*?)</a>',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = shan.str_extract('href="(.*?)">',part)
                # 输出数据
            yield item 
