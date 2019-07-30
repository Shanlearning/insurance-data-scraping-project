# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A中英人寿Spider(scrapy.Spider):
    name = '中英人寿'
    #http://www.aviva-cofco.com.cn/website/xxzx/gkxxpl/gsjbxx/cpbaclxxpl/grbxcp/list-1.shtml
    
    def start_requests(self):
        gx_urls = ['http://www.aviva-cofco.com.cn/website/xxzx/gkxxpl/gsjbxx/cpbaclxxpl/grbxcp/list-1.shtml'] #个险
        for url in gx_urls:        
                    yield scrapy.Request(url=url ,callback=self.gx_parse)
        
            
        tx_urls = ['http://www.aviva-cofco.com.cn/website/xxzx/gkxxpl/gsjbxx/cpbaclxxpl/ttbxcp/list-1.shtml']
        for url in tx_urls:       
                   yield scrapy.Request(url=url,callback=self.tx_parse)
                   
    def gx_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.li_content').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中英人寿'
                item['product_name'] = "中英" + shan.str_extract('中英(.*?)</a>',part)    
                item['product_sale_status'] = ""
                item['product_contract_link'] = "http://www.aviva-cofco.com.cn"+ shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        next_pages = re.findall("list-\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-1)]
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.gx_parse)
            
    def tx_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.li_content').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中英人寿'
                item['product_name'] = "中英" + shan.str_extract('中英(.*?)</a>',part)    
                item['product_sale_status'] = ""
                item['product_contract_link'] = "http://www.aviva-cofco.com.cn"+ shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        next_pages = re.findall("list-\d+[.]shtml",response.text)
        next_pages = next_pages[0:(len(next_pages)-1)]
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.tx_parse)