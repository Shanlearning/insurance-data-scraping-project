# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import  ProjectInsuranceScrapItem


class A中国平安Spider(scrapy.Spider):
    name = '中国平安'
    data = {'requestid': 'com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause',
            'SALES_STATUS': '03'}
    
    start_urls = "http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=03" 
    
    def parse(self, response):
        
        headers={'Accept': 'application/xml, text/xml, */*',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Content-Length': '0',
              'Cookie': 'BIGipServerPOOL_PACLOUD_PRDR2017082805794=353704364.46203.0000; WEBTRENDS_ID=4.0.4.33-834098624.30709981; WT-FPC=id=4.0.4.33-834098624.30709981:lv=1545412240729:ss=1545412240729:fs=1545409687808:pn=1:vn=2; WLS_HTTP_BRIDGE_ILIFE=BUTPLSlpCaxjv6KxwjIcbNCMRP2rNWZLOKVioW9memP82JAojXvy!-1766717560',
              'Host': 'life.pingan.com',
              'Origin': 'http://life.pingan.com',
              'Referer': 'http://life.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan_tingshouchanpin.jsp',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    
        url='http://life.pingan.com/life_insurance/elis.pa18.commonQuery.visit?requestid=com.palic.elis.pos.intf.biz.action.PosQueryAction.queryPlanClause&SALES_STATUS=03',
            
        yield scrapy.Request(
                url = url ,
                headers=headers ,
                callback = self.parse_ajax
                )
        

    def parse_ajax(self, response , cn_name=name):
        # 从每一行抽取数据
        
        #for part in response.css("map"):
            # 在售保险的内容输入
        #    item = ProjectInsuranceScrapItem()            
        #    item['company'] = cn_name
        #    item['product'] = part.css("CLAUSE_NAME::text").get(),
        #    item['status'] = part.css("PLAN_SALES_STATUS::text").get()
        #    item['contract_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO=' \
        #                             + part.css("VERSION_NO::text").get() + '&DOC_CODE=01'
        #    item['price_link'] = 'http://www.pingan.com/life_insurance/elis.intf.queryClauseContent.visit?VERSION_NO='   \
        #                             + part.css("VERSION_NO::text").get() + '&DOC_CODE=04'
            # 输出数据
            yield response.text
