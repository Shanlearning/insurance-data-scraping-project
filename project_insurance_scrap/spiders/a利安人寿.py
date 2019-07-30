# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A利安人寿Spider(scrapy.Spider):
    name = '利安人寿'
    #http://www.lianlife.com/cpjbxx/zscpxx/zsgxcp/

    def start_requests(self):
        zaishou_urls = ['http://www.lianlife.com/cpjbxx/zscpxx/zsgxcp/','http://www.lianlife.com/cpjbxx/zscpxx/zsgxcp/index_1.shtml', #个险 2
                        'http://www.lianlife.com/cpjbxx/zscpxx/zsybcp/', #银保 1
                        'http://www.lianlife.com/cpjbxx/zscpxx/zstxcp/', 'http://www.lianlife.com/cpjbxx/zscpxx/zstxcp/index_1.shtml','http://www.lianlife.com/cpjbxx/zscpxx/zstxcp/index_2.shtml', #团险 3
                        'http://www.lianlife.com/cpjbxx/zscpxx/zsxqdcp/'] #新渠道 1
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://www.lianlife.com/cpjbxx/tscpxx/tsgxcp/','http://www.lianlife.com/cpjbxx/tscpxx/tsgxcp/index_1.shtml','http://www.lianlife.com/cpjbxx/tscpxx/tsgxcp/index_2.shtml','http://www.lianlife.com/cpjbxx/tscpxx/tsgxcp/index_3.shtml', #个险 4
                         'http://www.lianlife.com/cpjbxx/tscpxx/tsybcp/','http://www.lianlife.com/cpjbxx/tscpxx/tsybcp/index_1.shtml','http://www.lianlife.com/cpjbxx/tscpxx/tsybcp/index_2.shtml','http://www.lianlife.com/cpjbxx/tscpxx/tsybcp/index_3.shtml','http://www.lianlife.com/cpjbxx/tscpxx/tsybcp/index_4.shtml', #银保 5
                         'http://www.lianlife.com/cpjbxx/tscpxx/tstxcp/','http://www.lianlife.com/cpjbxx/tscpxx/tstxcp/index_1.shtml', #团险 2
                         'http://www.lianlife.com/cpjbxx/tscpxx/tsxqdcp/','http://www.lianlife.com/cpjbxx/tscpxx/tsxqdcp/index_1.shtml', #新渠道 2
                         'http://www.lianlife.com/cpjbxx/tscpxx/tsjdcp/', #经代 1
                         'http://www.lianlife.com/cpjbxx/tscpxx/tsdxcp/' #电销 1
                         ]
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css('.lpcx_con a').extract()
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '利安人寿'
                item['product_sale_status'] = '在售'
                name = shan.str_extract('</span>(.*?)</a>',part) 
                if "条款" in name:
                    item['product_name'] = shan.str_extract('(.*?)条款',name)
                    item['product_contract_link'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
                elif "产品说明书" in name:
                    item['product_name'] = shan.str_extract('(.*?)产品说明书',name)
                    item['product_official_report_list'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
                else:
                    item['product_name'] = name
                    item['product_contract_link'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
                # 输出数据
                yield item 
                   
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = response.css('.lpcx_con a').extract()
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '利安人寿'
            item['product_sale_status'] = '停售'
            name = shan.str_extract('</span>(.*?)</a>',part) 
            if "条款" in name:
                item['product_name'] = shan.str_extract('(.*?)条款',name)
                item['product_contract_link'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
            elif "产品说明书" in name:
                item['product_name'] = shan.str_extract('(.*?)产品说明书',name)
                item['product_official_report_list'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
            else:
                item['product_name'] = name
                item['product_contract_link'] = "http://www.lianlife.com"+ shan.str_extract('href="../../..(.*)">',part)
                # 输出数据
            yield item 

                   