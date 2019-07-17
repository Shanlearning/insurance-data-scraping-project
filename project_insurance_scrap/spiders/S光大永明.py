# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A光大永明Spider(scrapy.Spider):
    name = '光大永明'
    #http://www.sunlife-everbright.com/sleb/info/jbxx/cpjbxx/cpxxp/468a89fa-1.html
    
    def start_requests(self):
        #
        urls = ['http://www.sunlife-everbright.com/sleb/info/jbxx/cpjbxx/cpxxp/468a89fa-1.html']
        
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Cookie': 'UM_distinctid=16bf88a1698404-01cafbdd88510b-37647e05-13c680-16bf88a169975c; CNZZDATA1274208563=1695324027-1563242927-%7C1563352631',
                  'Host': 'www.sunlife-everbright.com',
                  'If-Modified-Since': 'Wed, 03 Jul 2019 07:18:28 GMT',
                  'If-None-Match': "4a89-58cc1aaf03900-gzip",
                  'Referer': 'http://www.sunlife-everbright.com/sleb/info/jbxx/cpjbxx/cpxxp/468a89fa-10.html',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                  }

        for url in urls:
            yield scrapy.Request(url=url, headers= header ,callback=self.parse)
    
    def parse(self, response):
         # 从每一行抽取数据
        result =  response.css('.news_list a').extract()
        for part in result:
                # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()
                item['company_name'] = '光大永明'
                item['product_name'] = shan.str_extract('title="(.*?)"',part)
                item['product_sale_status'] = ''
                contract_link = re.findall('href="(.*?)" ', part)[0]
                if "https://" not in contract_link:
                    contract_link = "http://www.sunlife-everbright.com" + contract_link
                    yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
                else:
                    item['product_contract_link'] = contract_link
                    # 输出数据
                    yield item
                    
        # 找到下一页的代码
        a = str(response.css('.pagingNormal').extract())
        next_pages = re.findall("/sleb/info/jbxx/cpjbxx/cpxxp/468a89fa-\d+[.]html",a)
        for next_page in next_pages:
            yield response.follow("http://www.sunlife-everbright.com"+next_page, callback=self.parse)

    def contract_parse(self, response):
        result = response.css("tr")
        result = result[1:len(result)].extract()
        item = response.meta['item']
        a = shan.str_keep('材料清单',result)
        if 'pdf' in a: 
            item['product_official_report_list'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',a) 
        else: 
            item['product_official_report_list'] = ''
        b = shan.str_keep('费率',result)
        if 'pdf' in b: 
            item['product_price_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',b) 
        else:
            item['product_price_link'] =''
        c = shan.str_keep('条款',result)
        if 'pdf' in c: 
            item['product_contract_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',c) 
        else:
            item['product_contract_link'] = ''
        d = shan.str_keep('价值表（全表）',result)
        if 'xlsx' in d: 
            item['product_pv_full_list_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',d) 
        else:
            item['product_pv_full_list_link'] = ''
        e = shan.str_keep('价值表（示例）',result)  
        if 'pdf' in e: 
            item['product_pv_example_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',e) 
        else:
            item['product_pv_example_link'] = ''
        f = shan.str_keep('总精算师',result)  
        if 'pdf' in f: 
            item['product_chief_actuary_claim_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',f) 
        else:
            item['product_chief_actuary_claim_link'] =''
        g = shan.str_keep('法律责任人',result)  
        if 'pdf' in g: 
            item['prodcct_law_response_link'] = "http://www.sunlife-everbright.com" + shan.str_extract('href="(.*?)"',g)
        else:
            item['prodcct_law_response_link'] = ''
        yield item
            
        
        
    