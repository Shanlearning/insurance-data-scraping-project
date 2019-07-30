# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A平安养老Spider(scrapy.Spider):
    name = '平安养老'
    #http://yl.pingan.com/px/informationDisclosure/insuranceProductList.shtml
    

    def start_requests(self):
        urls = ['http://yl.pingan.com/px/informationDisclosure/insuranceProductList.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.news_list a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem() 
                item['product_id'] = shan.str_extract('title="(.*?)平安',part)
                item['company_name'] = '平安养老'
                name = shan.str_extract('平安(.*?)</a>',part) 
                if "条款" in name:
                    item['product_name'] = "平安" + shan.str_extract('(.*?)条款',name)
                else:
                    item['product_name'] = "平安" + name
                item['product_sale_status'] = ' 在售'
                item['product_contract_link'] = shan.str_extract('href="(.*?)" title',part)
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        page = response.css('li.page').extract()
        next_pages = shan.str_extract("/px/informationDisclosure/insuranceProductList_\d+[.]shtml",page)
        for next_page in next_pages:
            yield response.follow("http://yl.pingan.com" + next_page, callback=self.parse)