# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A泰康养老Spider(scrapy.Spider):
    name = '泰康养老'
    #http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list.html

    def start_requests(self):
        zaishou_urls = ['http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list.html',
                        'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list_2.html',
                        'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list_3.html',
                        'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list_4.html',
                        'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list_5.html'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/tstk/list.html',
                         'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/tstk/list_2.html']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('li').extract()
        result = shan.str_keep('条款',result) 
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '泰康养老'
                item['product_name'] = shan.str_extract('《(.*?)》',part)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://tkyl.pension.taikang.com"+ shan.str_extract('href="(.*)" target',part)
                # 输出数据
                yield item 
                
        
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('li').extract()
        result = shan.str_keep('条款',result) 
        result = result[1:len(result)]
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '泰康养老'
            item['product_name'] = shan.str_extract('《(.*?)》',part)
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://tkyl.pension.taikang.com"+ shan.str_extract('href="(.*)" target',part)
            
            # 输出数据
            yield item 

        