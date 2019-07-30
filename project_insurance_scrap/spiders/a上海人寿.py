# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A上海人寿Spider(scrapy.Spider):
    name = '上海人寿'
    #http://www.shanghailife.com.cn/cpzx/cptk/zscp/

    def start_requests(self):
        zaishou_urls = ['http://www.shanghailife.com.cn/cpzx/cptk/zscp/'] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.shanghailife.com.cn/cpzx/cptk/tscp/']
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.pro_list a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '上海人寿'
                item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
                item['product_sale_status'] = '在售'
                contract_link = shan.str_extract('href="(.*)" target',part)
                yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
             
        
                
        next_pages = response.css('.page').extract()
        next_pages = shan.str_extract('"下一页" href="(.*?)">下一页',next_pages)
        for next_page in next_pages:
            if "#" not in next_page:
                yield response.follow(next_page, callback=self.zaishou_parse)
                
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.pro_list a').extract()
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '上海人寿'
            item['product_name'] = shan.str_extract('>(.*?)</a>',part) 
            item['product_sale_status'] = '停售'
            contract_link = shan.str_extract('href="(.*)" target',part)
            yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
            
            


        next_pages = response.css('.page').extract()
        next_pages = shan.str_extract('"下一页" href="(.*?)">下一页',next_pages)
        for next_page in next_pages:
            if "#" not in next_page:
                yield response.follow(next_page, callback=self.tingshou_parse) 
                
                
    def contract_parse(self, response):
        result = response.css("p").extract()
        item = response.meta['item']
        a = shan.str_keep('产品',result)
        if 'jsp' in a: 
            item['product_official_report_list'] = shan.str_extract('href="(.*?)"><span',a) 
        else: 
            item['product_official_report_list'] = ''
        b = shan.str_keep('费率',result)
        if 'jsp' in b: 
            item['product_price_link'] = shan.str_extract('href="(.*?)"><span',b) 
        else:
            item['product_price_link'] =''
        c = shan.str_keep('条款',result)
        if 'jsp' in c: 
            item['product_contract_link'] = shan.str_extract('href="(.*?)"><span',c) 
        else:
            item['product_contract_link'] = ''
        d = shan.str_keep('价值表',result)
        if 'jsp' in d: 
            item['product_pv_full_list_link'] = shan.str_extract('href="(.*?)"><span',d) 
        else:
            item['product_pv_full_list_link'] = ''
        f = shan.str_keep('总精算师',result)  
        if 'jsp' in f: 
            item['product_chief_actuary_claim_link'] = shan.str_extract('href="(.*?)"><span',f) 
        else:
            item['product_chief_actuary_claim_link'] =''
        g = shan.str_keep('法律责任人',result)  
        if 'jsp' in g: 
            item['prodcct_law_response_link'] =  shan.str_extract('href="(.*?)"><span',g)
        else:
            item['prodcct_law_response_link'] = ''
        yield item

        
        
                   