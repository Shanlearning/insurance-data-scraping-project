# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
#import re

class A交银康联Spider(scrapy.Spider):
    name = '交银康联'
    #https://www.bocommlife.com/sites/main/twainindex/xxpl.htm?columnid=297&page=1
    
    def start_requests(self):
        #
        urls = ['https://www.bocommlife.com/sites/main/twainindex/xxpl.htm?columnid=297&page=1']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 从每一行抽取数据
        result = shan.str_keep("险",response.css("tr").extract()) 
        result = result[1:len(result)]
        zs_result = result[shan.which(shan.str_detect("在售", result)[0]):shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[shan.which(shan.str_detect("停售", result)[0]):len(result)]

        zs_result = shan.str_keep('style="text-align: center"',zs_result) 
        zs_result =  shan.str_keep('(寿|保)险',zs_result)

        ts_result = shan.str_keep('style="text-align: center',ts_result)
        ts_result = shan.str_keep('(寿|保)险', ts_result)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'
            item['product_type'] = ''
            #a=shan.str_keep("险",re.findall("<p.+p>",part))
            #item['product_name'] =  shan.str_extract(">(.*)<",a)
            a= shan.str_extract('\S+险',part)
            item['product_name'] =  shan.str_extract('>?\S+险',a) 
            item['product_sale_status'] = '在售'

            item['product_contract_link'] = "www.bocommlife.com"+shan.str_keep("/",shan.str_extract('href="(.*?)">',part))
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item
            
        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'
            item['product_type'] = ''
            #a=shan.str_keep("险",re.findall("<p.+p>",part))
            #item['product_name'] =  shan.str_extract(">(.*)<",a)
            a= shan.str_extract('\S+险',part)
            item['product_name'] =  shan.str_extract('>?\S+险',a) 
            item['product_sale_status'] = '停售'

            item['product_contract_link'] = "www.bocommlife.com"+shan.str_keep("/",shan.str_extract('href="(.*?)">',part))
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item
        