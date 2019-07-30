# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A中邮人寿Spider(scrapy.Spider):
    name = '中邮人寿'
    #http://www.chinapost-life.com/export/xxpl/index.html

    def start_requests(self):
        zaishou_urls = ['http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/ffy/index.html',
                        'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/llt/index.html',
                        'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/mms/index.html',
                        'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/gljy/index.html',
                        'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/nnh/index.html',
                        'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/qtbx/index.html'
                        ] 
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
        tingshou_urls = ['http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/ts/index.html',
                         'http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/ts/index.html_319159481.html'
                         ]
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
                   
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
        weishou_urls = ['http://www.chinapost-life.com/export/xxpl/baoxianchanpinxinxi/ws/index.html']
        for url in weishou_urls:       
                   yield scrapy.Request(url=url,callback=self.weishou_parse)
        
            
       
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.grey2').extract()
        result = shan.str_keep('险',result)
        if type(result) == str: 
            result = [result]
        else:
            result = result
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '中邮人寿'
                item['product_name'] = shan.str_extract('\r\n\t\t\t\t(.*?)\r\n\t\t\t',part) 
                item['product_sale_status'] = '在售'
                contract_link = "http://www.chinapost-life.com"+ shan.str_extract('href="(.*)" class',part)
                yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
                # 输出数据
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.grey2').extract()
        result = shan.str_keep('险',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中邮人寿'
            item['product_name'] = shan.str_extract('\r\n\t\t\t\t(.*?)\r\n\t\t\t',part) 
            item['product_sale_status'] = '停售'
            contract_link = "http://www.chinapost-life.com"+ shan.str_extract('href="(.*)" class',part)
            yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
            
    def weishou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.grey2').extract()
        result = shan.str_keep('险',result)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中邮人寿'
            item['product_name'] = shan.str_extract('\r\n\t\t\t\t(.*?)\r\n\t\t\t',part) 
            item['product_sale_status'] = '未售'
            contract_link = "http://www.chinapost-life.com"+ shan.str_extract('href="(.*)" class',part)
            yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
                
  
                
    def contract_parse(self, response):
        result = response.css(".articleShowText a").extract()
        item = response.meta['item']
        a = shan.str_keep('产品',result)
        if 'pdf' in a: 
            item['product_official_report_list'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',a) 
        else: 
            item['product_official_report_list'] = ''
        b = shan.str_keep('费率',result)
        if 'pdf' in b: 
            item['product_price_link'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',b) 
        else:
            item['product_price_link'] =''
        c = shan.str_keep('条款',result)
        if 'pdf' in c: 
            item['product_contract_link'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',c) 
        else:
            item['product_contract_link'] = ''
        d = shan.str_keep('价值表',result)
        if 'pdf' in d: 
            item['product_pv_full_list_link'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',d) 
        else:
            item['product_pv_full_list_link'] = ''
        f = shan.str_keep('总精算师',result)  
        if 'pdf' in f: 
            item['product_chief_actuary_claim_link'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',f) 
        else:
            item['product_chief_actuary_claim_link'] =''
        g = shan.str_keep('法律责任人',result)  
        if 'pdf' in g: 
            item['prodcct_law_response_link'] = "http://www.chinapost-life.com" + shan.str_extract('href="(.*?)"',g)
        else:
            item['prodcct_law_response_link'] = ''
        yield item

