# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A国富人寿Spider(scrapy.Spider):
    name = '国富人寿'
    #https://www.e-guofu.com/cms_mysql_pro/information1/base/opi/index.jsp

    def start_requests(self):
        urls = ['https://www.e-guofu.com/cms_mysql_pro/information1/base/opi/index.jsp',
                'https://www.e-guofu.com/cms_mysql_pro/information1/base/opi/index_2.jsp'
                ] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('li').extract()
        result = shan.str_keep('国富',result)
        result = result[1:len(result)]
        for part in result:
                 # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '国富人寿'
            item['product_name'] = shan.str_extract('国.*?险',part)
            item['product_sale_status'] = ''
            contract_link = "https://www.e-guofu.com/cms_mysql_pro/information1/base/opi/" + shan.str_extract('href="(.*?)">',part) 
            yield response.follow(contract_link, callback= self.contract_parse , meta=({'item': item}) )
                # 输出数据

            
    def contract_parse(self, response):
        result = response.css(".detail a").extract()
        item = response.meta['item']
        c = shan.str_keep('条款',result)
        if len(c) ==1:
            c = c
        if len(c) ==2:
            c = c[1]
        item['product_contract_link'] = "https://www.e-guofu.com" + shan.str_extract('href="(.*?)" target',c) 
        yield item