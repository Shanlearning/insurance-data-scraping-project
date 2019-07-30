# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

class A国华人寿Spider(scrapy.Spider):
    name = '国华人寿'
    #http://www.95549.cn/pages/intro/xxpl_detail03.shtml

    def start_requests(self):
        urls = ['http://www.95549.cn/pages/intro/xxpl_detail03.shtml'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('.bxContent').extract()
        result = re.split('查看',result[0]) 
        result = shan.str_keep('国华',result)
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '国华人寿'
            item['product_name'] = "国华" + shan.str_extract('国华(.*?)</p>',part)
            item['product_sale_status'] = ''
            link = shan.str_extract('href="(.*?)" target',part)
            if "content" not in link:
                contract_link = "http://www.95549.cn/pages/intro/" + link
                yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
            else:
                link1 = link + "z"
                item['product_contract_link'] = "http://www.95549.cn/pages/"+ shan.str_extract('../(.*?)z',link1) 
                # 输出数据
                yield item 
            
            
    def contract_parse(self, response):
        result = response.css("p").extract() 
        result = shan.str_keep('国华',result)
        result = result[1:len(result)]
        item = response.meta['item']
        a = shan.str_keep('材料清单',result)
        if 'pdf' in a: 
            item['product_official_report_list'] = "http://www.95549.cn/pages/intro/" + shan.str_extract('href="(.*?)"',a) 
        else: 
            item['product_official_report_list'] = ''
        b = shan.str_keep('费率|金额',result)
        if 'pdf' in b: 
            item['product_price_link'] = "http://www.95549.cn/pages/intro/" + shan.str_extract('href="(.*?)"',b) 
        else:
            item['product_price_link'] =''
        c = shan.str_keep('条款',result)
        if 'pdf' in c: 
            item['product_contract_link'] = "http://www.95549.cn/pages/intro/" + shan.str_extract('href="(.*?)"',c) 
        else:
            item['product_contract_link'] = ''
        f = shan.str_keep('总精算师',result)  
        if 'pdf' in f: 
            item['product_chief_actuary_claim_link'] = "http://www.95549.cn/pages/intro/" + shan.str_extract('href="(.*?)"',f) 
        else:
            item['product_chief_actuary_claim_link'] =''
        g = shan.str_keep('法律责任人',result)  
        if 'pdf' in g: 
            item['prodcct_law_response_link'] = "http://www.95549.cn/pages/intro/" + shan.str_extract('href="(.*?)"',g)
        else:
            item['prodcct_law_response_link'] = ''
        yield item
