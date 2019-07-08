# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem

class A中国平安Spider(scrapy.Spider):
    name = '中国平安'
    
    start_urls = ['http://life.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan.jsp']
    
    
    def parse(self):
        # 输入在售保险的第一页网址
        url = "http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=03" 
        
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
        
        yield scrapy.Request(url, callback=self.parse_ajax,
                             headers = header,       
                             dont_filter=True)
    
    def parse_ajax(self, response):
         #从每一行抽取数据
        
        for part in response.css("map"):
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company'] = '中国平安'
            item['product'] = part.css("CLAUSE_NAME::text").get(),
            item['status'] = part.css("PLAN_SALES_STATUS::text").get()
            item['contract_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO=' \
                                     + part.css("VERSION_NO::text").get() + '&DOC_CODE=01'
            item['price_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO='   \
                                     + part.css("VERSION_NO::text").get() + '&DOC_CODE=04'
            # 输出数据
            yield item
