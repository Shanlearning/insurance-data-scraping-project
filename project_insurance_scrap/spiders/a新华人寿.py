# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrapfunctions as shan

class A新华人寿Spider(scrapy.Spider):
    name = '新华人寿'
    
    #https://www.newchinalife.com/node/372
    
    def start_requests(self):
        #
        urls = ['https://www.newchinalife.com/node/372']#健康保障托管业务
       
        for url in urls:       
                   yield scrapy.Request(url=url,callback=self.parse)
                   
    def parse(self, response):
         # 从每一行抽取数据
        result =  response.css('tr').getall()
        result =  result[1:len(result)]
        for part in result:
                # 在售保险的内容输入
                part = re.findall('<td>(.*)</td>', part)

                item = ProjectInsuranceScrapItem()
                item['company_name'] = '新华人寿'
                item['product_type'] = part[2]

                item['product_sale_status'] = part[3]
                contract_link = re.findall('href="(.*)?" ', part[4])[0]
                if "https://" not in contract_link:
                    contract_link = "https://www.newchinalife.com" + contract_link
                    yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
                else:
                    item['product_name'] = part[1]
                    item['product_contract_link'] = contract_link
                    # 输出数据
                    yield item
        # 找到下一页的代码
        next_pages = re.findall("/node/372_\d+",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse)

    def contract_parse(self, response):
        result = response.css("tr")
        result = result[1:len(result)].extract()
        for part in result:
            item = response.meta['item']
            part = re.findall('<td>(.*)</td>', part)

            item['product_name'] = shan.str_extract('>(.*?)</a>',part[1])
            item['product_special_status'] = part[2]
            item['product_contract_link'] = shan.str_extract('href="(.*?)"',part[1])
            # 输出数据
            yield item
    
    
    
    
    