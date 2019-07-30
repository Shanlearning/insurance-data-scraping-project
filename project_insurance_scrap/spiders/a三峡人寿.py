# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A三峡人寿Spider(scrapy.Spider):
    name = '三峡人寿'
    #http://www.tg-life.com.cn/bxcpmljtk/75.html?sale_status=1

    def start_requests(self):
        zaishou_urls = ['http://www.tg-life.com.cn/bxcpmljtk/75.html?sale_status=1'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.tg-life.com.cn/bxcpmljtk/75.html?sale_status=2']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('三峡',result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '三峡人寿'
                item['product_name']  = "三峡" + shan.str_extract('三峡(.*?)</td>',part) 
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.tg-life.com.cn"+ shan.str_extract('href="(.*)" target',part)
                item['product_price_link'] = "http://www.tg-life.com.cn"+ shan.str_extract('条款</a></td>\r\n\t\t\t\t\t\t\t\t<td align="center"><a href="(.*)" target',part)
                # 输出数据
                yield item 
                
        a = response.css('a~ a+ a').extract()
        a = shan.str_keep('下一页',a) 
        b = shan.str_extract('href="(.*?)">',a) 
        yield response.follow("http://www.tg-life.com.cn" + b, callback=self.zaishou_parse)       
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = shan.str_keep('三峡',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '三峡人寿'
            item['product_name']  = "三峡" + shan.str_extract('三峡(.*?)</td>',part) 
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://www.tg-life.com.cn"+ shan.str_extract('href="(.*)" target',part)
            item['product_price_link'] = "http://www.tg-life.com.cn"+ shan.str_extract('条款</a></td>\r\n\t\t\t\t\t\t\t\t<td align="center"><a href="(.*)" target',part)
                # 输出数据
            yield item 

        a = response.css('a~ a+ a').extract()
        a = shan.str_keep('下一页',a) 
        b = shan.str_extract('href="(.*?)">',a) 
        yield response.follow("http://www.tg-life.com.cn" + b, callback=self.tingshou_parse)
                   