# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A吉祥人寿Spider(scrapy.Spider):
    name = '吉祥人寿'
    #http://www.jxlife.com.cn/web/info/basicinfo/prtlistfolder/index.jsp

    def start_requests(self):
        urls = ['http://www.jxlife.com.cn/web/info/basicinfo/prtlistfolder/index.jsp'] 
        for url in urls:        
            yield scrapy.Request(url=url ,callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('tr').extract()
        result = result[2:len(result)]
        
        zs_result = shan.str_keep('data-isstate="1"',result)
        ts_result = shan.str_keep('data-isstate="2"',result)
        ds_result = shan.str_keep('data-isstate="3"',result)
        
        for part in zs_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '吉祥人寿'
                item['product_name'] = shan.str_extract('class="td_body">(.*?)</td>',part)  
                item['product_sale_status'] = "在售" 
                item['product_contract_link'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)pdf"',part) + "pdf"
                item['product_official_report_list'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)" target="_blank" style="cursor: hand; text-decoration: underline;">\n\t\t\t\t\t\t\t\t\t\t\t\t<font color="blue">其他备案资料</font>',part) 
                # 输出数据
                yield item 
                
        for part in ts_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '吉祥人寿'
                item['product_name'] = shan.str_extract('class="td_body">(.*?)</td>',part) 
                item['product_sale_status'] = "停售" 
                item['product_contract_link'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)pdf"',part) + "pdf"  
                item['product_official_report_list'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)" target="_blank" style="cursor: hand; text-decoration: underline;">\n\t\t\t\t\t\t\t\t\t\t\t\t<font color="blue">其他备案资料</font>',part) 
                # 输出数据
                yield item 
                
        for part in ds_result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '吉祥人寿'
                item['product_name'] = shan.str_extract('class="td_body">(.*?)</td>',part) 
                item['product_sale_status'] = "待售" 
                item['product_contract_link'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)pdf"',part) + "pdf"  
                item['product_official_report_list'] = "http://www.jxlife.com.cn" + shan.str_extract('href="(.*)" target="_blank" style="cursor: hand; text-decoration: underline;">\n\t\t\t\t\t\t\t\t\t\t\t\t<font color="blue">其他备案资料</font>',part) 
                # 输出数据
                yield item 