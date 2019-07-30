# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan


class A同方人寿Spider(scrapy.Spider):
    name = '同方人寿'
    #http://opid.aegonthtf.com/desk/productInfo.do#tk-tag1
    

    def start_requests(self):
        urls = ['http://opid.aegonthtf.com/desk/productInfo.do#tk-tag1'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result =  result[1:len(result)]
        zs_result = result[0:shan.which(shan.str_detect("产品名称", result))[1]]
        ts_result = result[shan.which(shan.str_detect("产品名称", result))[1]:(len(result)-2)]
        
        zs_result = shan.str_keep('险',zs_result) 
        ts_result = shan.str_keep('险',ts_result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '同方人寿'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = "http://opid.aegonthtf.com/"+ shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '同方人寿'
                item['product_name'] = shan.str_extract('<td>(.*?)</td>',part)  
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = "http://opid.aegonthtf.com/"+ shan.str_extract('href="(.*)"',part)
                # 输出数据
                yield item 
      