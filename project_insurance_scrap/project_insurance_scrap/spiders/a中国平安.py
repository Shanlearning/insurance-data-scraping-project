# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem

class A中国平安Spider(scrapy.Spider):
    name = '中国平安'
    
    #http://life.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan.jsp
    
    def start_requests(self):
        danren_urls = [
            'http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=01',
            'http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=02',
            'http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=03',        
        ]
        
        group_urls = ['http://life.pingan.com/gongkaixinxipilu_xml/tingshou_tuanxian.xml',  
                      'http://life.pingan.com/gongkaixinxipilu_xml/zaishou_tuanxian.xml',
        ]
        
        header = {'Accept': 'application/xml, text/xml, */*',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Connection': 'keep-alive',
                  'Content-Length': '0',
                  'Cookie': 'WLS_HTTP_BRIDGE_ILIFE=5IbOgMk_9kL96ragu0DKb38Nw6DdA3-HRpW3Qa2NbcFQdYxxlu4s!-1766717560; BIGipServerPOOL_PACLOUD_PRDR2017082805794=353704364.46203.0000',
                  'Host': 'life.pingan.com',
                  'Origin': 'http://life.pingan.com',
                  'Referer': 'http://life.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan.jsp',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest'}
        
        for url in danren_urls:
            yield scrapy.Request(url=url, headers = header , callback=self.dan_parse)
        for url in group_urls:
            yield scrapy.Request(url=url , callback=self.group_parse)
            
    def dan_parse(self, response):
         #从每一行抽取数据       
        for part in response.css("map"):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中国平安'
        
            item['product_type'] = part.css("PLAN_SALES_CHANNEL::text").get()
            item['product_id'] = part.css("PLAN_CODE::text").get()
            item['product_name'] = part.css("CLAUSE_NAME::text").get()
            item['product_sale_status'] = part.css("PLAN_SALES_STATUS::text").get()
            
            item['product_contract_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO=' \
                                     + part.css("VERSION_NO::text").get() + '&DOC_CODE=01'
            item['product_price_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO='   \
                                     + part.css("VERSION_NO::text").get() + '&DOC_CODE=04'
                                     
            item['product_start_date'] =  part.css("START_DATE::text").get()
            item['product_end_date'] = part.css("END_DATE::text").get()  
            # 输出数据
            yield item
            
    def group_parse(self, response):
         #从每一行抽取数据       
        for part in response.css("map"):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '中国平安'
        
            item['product_type'] = part.css("PLAN_SALES_CHANNEL::text").get()
            item['product_id'] = part.css("PLAN_CODE::text").get()
            item['product_name'] = part.css("CLAUSE_NAME::text").get()
            item['product_sale_status'] = part.css("PLAN_SALES_STATUS::text").get()
            item['product_contract_link'] = 'http://life.pingan.com' + part.css("LINK_URL::text").get()
            
            item['product_start_date'] =  part.css("START_DATE::text").get()
            item['product_end_date'] = part.css("END_DATE::text").get()  
            # 输出数据
            yield item       
            
            
            
            
            
            
            
            
            
            
            
            
            
            