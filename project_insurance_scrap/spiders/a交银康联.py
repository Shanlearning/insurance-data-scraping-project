# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

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
        zs_result = result[shan.which(shan.str_detect("在售", result))[0]:shan.which(shan.str_detect("停售", result))[0]]
        ts_result = result[shan.which(shan.str_detect("停售", result))[0]:len(result)]

        zs_result =  shan.str_keep('交银',zs_result)
        ts_result = shan.str_keep('交银', ts_result)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'
            if "附加交银" in part:
                item['product_name'] =  "附加交银" + shan.str_extract('附加交银(.*?)</',part)
            else:
                item['product_name'] =  "交银" + shan.str_extract('交银(.*?)</',part)
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "www.bocommlife.com"+shan.str_extract('href="(.*?)">',part)
            # 输出数据
            yield item
            
        for part in ts_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            item['company_name'] = '交银康联'
            if "附加交银" in part:
                item['product_name'] =  "附加交银" + shan.str_extract('附加交银(.*?)<',part)
            else:
                item['product_name'] =  "交银" + shan.str_extract('交银(.*?)</',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "www.bocommlife.com"+shan.str_extract('href="(.*?)">',part)
            # 输出数据
            yield item
        