# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A农银人寿Spider(scrapy.Spider):
    name = '农银人寿'
    #http://www.abchinalife.cn/cms-web/front/abchinalife/xxpl/jbxx/cpmljtk/zscpmljtk/zscpmljtk@1.html

    def start_requests(self):
        zaishou_urls = ['http://www.abchinalife.cn/cms-web/front/abchinalife/xxpl/jbxx/cpmljtk/zscpmljtk/zscpmljtk@1.html'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.abchinalife.cn/cms-web/front/abchinalife/xxpl/jbxx/cpmljtk/tscpmljtk/tscpmljtk@1.html']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.dis_proboxul a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '农银人寿'
                name = shan.str_extract('>·(.*?)</a>',part) 
                if "条款" in name:
                    item['product_name'] = shan.str_extract('(.*?)条款',name)
                elif "合同" in name:
                    item['product_name'] = shan.str_extract('(.*?)产品合同',name)
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://www.abchinalife.cn"+ shan.str_extract('href="(.*)" target',part)
                # 输出数据
                yield item 
                
        a = response.css('option').extract()
        b = shan.str_extract('value="(.*?)">',a)
        b = b[1:len(b)]
        for part in b:
            yield response.follow("http://www.abchinalife.cn" + part, callback=self.zaishou_parse)       
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.dis_proboxul a').extract()
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '农银人寿'
            name =shan.str_extract('>·(.*?)</a>',part)
            if "条款" in name:
                item['product_name'] = shan.str_extract('(.*?)条款',name)
            elif "产品说明书" in name:
                item['product_name'] = shan.str_extract('(.*?)产品',name)
            else:
                item['product_name'] = name
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://www.abchinalife.cn"+ shan.str_extract('href="(.*)" target',part)
            
            # 输出数据
            yield item 

        a = response.css('option').extract()
        b = shan.str_extract('value="(.*?)">',a)
        b = b[1:len(b)]
        for part in b:
            yield response.follow("http://www.abchinalife.cn" + part, callback=self.tingshou_parse)       
                   