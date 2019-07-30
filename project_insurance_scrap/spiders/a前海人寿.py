# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A前海人寿Spider(scrapy.Spider):
    name = '前海人寿'
    #https://www.foresealife.com/publish/main/xxpl/60/85/01/ea9fb409-5830-4f7a-bb3c-6c5b4167c9c6/index.html

    def start_requests(self):
        zaishou_urls = ['https://www.foresealife.com/publish/main/xxpl/60/85/01/ea9fb409-5830-4f7a-bb3c-6c5b4167c9c6/index.html', #个险
                        'https://www.foresealife.com/publish/main/xxpl/60/85/01/5e12e4cc-b519-439d-9dcf-1e400c2a16b0/index.html']  #团险
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['https://www.foresealife.com/publish/main/xxpl/60/85/02/c854c6a8-14ec-4e9a-819b-2571139e9ff1/index.html',  #个险
                         'https://www.foresealife.com/publish/main/xxpl/60/85/02/55295971-c7d2-4abf-86a0-8102aa99f646/index.html']  #团险
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '前海人寿'
                item['product_name'] = shan.str_extract('\t\t\t\t\t(.*?)\t\t\t\t</td>',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "https://www.foresealife.com"+ shan.str_extract('href="(.*)">点击查看</a> \t\t\t\t</td>\t\t\t\t<td style="text-align:center;">',part)
                # 输出数据
                yield item 
                
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '前海人寿'
            item['product_name'] = shan.str_extract('\t\t\t\t\t(.*?)\t\t\t\t</td>',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "https://www.foresealife.com"+ shan.str_extract('href="(.*)">点击查看</a> \t\t\t\t</td>\t\t\t\t<td style="text-align:center;">',part)
            
            # 输出数据
            yield item 
