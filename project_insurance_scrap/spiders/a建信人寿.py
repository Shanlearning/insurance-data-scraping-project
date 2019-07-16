# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrapfunctions as shan
import numpy as np


class A建信人寿Spider(scrapy.Spider):
    name = '建信人寿'
    #http://www.ccb-life.com.cn/gkxxpl/jbxx/cpjbxx/14165.shtml?timestamp=1563174726724
    
    def start_requests(self):
        
        urls = ['http://www.ccb-life.com.cn/gkxxpl/jbxx/cpjbxx/14165.shtml?timestamp=1563174726724']
        for url in urls:        
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        # 从每一行抽取数据
        
        result =  response.css('tr').extract()

        zs_result = result[shan.which(shan.str_detect("在售", result)[0]):shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[shan.which(shan.str_detect("停售", result)[0]):len(result)]

        zs_result = shan.str_keep('class="(xl85|xl83)"',zs_result)
        zs_result =  shan.str_keep('(寿|保)险',zs_result)

        ts_result = shan.str_keep('class="(xl85|xl83)"',ts_result)
        ts_result = shan.str_keep('(寿|保)险', ts_result)

        for part in zs_result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '建信人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            a = shan.str_extract('\S+险',part)

            item['product_name'] = shan.str_extract('>(.*?)险',a)+"险"   
            item['product_sale_status'] = '在售'

            item['product_contract_link'] = "http://www.ccb-life.com.cn/upload"+shan.str_keep("pdf",shan.str_extract('upload(.*?)">',part))
            
            item['product_price_link'] = ''
            
            item['product_start_date'] = ''
            item['product_end_date'] = ''  
                # 输出数据
            if( shan.str_keep("pdf",shan.str_extract('upload(.*?)">',part)) != ''):
                yield item

        for part in ts_result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '建信人寿'

            item['product_type'] = ''
            item['product_id'] = ''
            a = shan.str_keep("险", shan.str_extract('\S+险', part))
            item['product_name'] = shan.str_extract('>(.*?)险', a) + "险"
            item['product_sale_status'] = '停售'

            item['product_contract_link'] = "http://www.ccb-life.com.cn/upload" + shan.str_keep("pdf", shan.str_extract(
                'upload(.*?)">', part))

            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            if (shan.str_keep("pdf", shan.str_extract('upload(.*?)">', part)) != ''):
                yield item