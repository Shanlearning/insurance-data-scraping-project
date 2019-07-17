# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re
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
        result = shan.str_keep("交银|险",response.css("tr").extract())

        zs_result = result[shan.which(shan.str_detect("在售", result))[0] : shan.which(shan.str_detect("停售", result))[0] ]
        ts_result = result[shan.which(shan.str_detect("停售", result))[0] :len(result)]

        zs_result = shan.str_drop('在售',zs_result)
        ts_result = shan.str_drop('停售',ts_result)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'

            part = re.findall(">(.*)<",part)

            item['product_name'] =  re.sub(" ","",shan.str_keep("交银|险", part))
            item['product_sale_status'] = '在售'

            item['product_contract_link'] = "www.bocommlife.com"+shan.str_keep("/",shan.str_extract('href="(.*?)">',part))

            # 输出数据
            yield item
            
        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'

            part = re.findall(">(.*)<",part)

            item['product_name'] = re.sub(" ","",shan.str_keep("交银|险", part))
            item['product_sale_status'] = '停售'

            item['product_contract_link'] = "www.bocommlife.com"+shan.str_keep("/",shan.str_extract('href="(.*?)">',part))

            # 输出数据
            yield item
        