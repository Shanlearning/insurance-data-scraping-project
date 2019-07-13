# -*- coding: utf-8 -*-
import scrapy
import re
from project_insurance_scrap.items import  ProjectInsuranceScrapItem

class A太保人寿Spider(scrapy.Spider):
    name = "太保人寿"
    
    #http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/?subMenu=1&inSub=3
    
    def start_requests(self):
        
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Connection': 'keep-alive',                  
                  'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216bd0179136167-058682b7032ad5-7a1437-1327104-16bd01791376a1%22%2C%22%24device_id%22%3A%2216bd0179136167-058682b7032ad5-7a1437-1327104-16bd01791376a1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; cpic_search_keywords=%u516C%u5F00%u4FE1%u606F%u62AB%u9732; s_fid=2D40D5ABB1419D0A-156B4470E510F1ED; s_cc=true; mbox=session#806a561f322a451ebc98140a94529a86#1562834304|PC#806a561f322a451ebc98140a94529a86.22_16#1564042044|check#true#1562832504; s_nr=1562832459880; s_sq=cpic-out%2520of%2520service%3D%2526c.%2526a.%2526activitymap.%2526page%253D%2525E7%2525AB%252599%2525E5%252586%252585%2525E6%252590%25259C%2525E7%2525B4%2525A2%2525E7%2525BB%252593%2525E6%25259E%25259C%2525E9%2525A1%2525B5%2526link%253D%2525E5%2525A4%2525AA%2525E5%2525B9%2525B3%2525E6%2525B4%25258B%2525E4%2525BF%25259D%2525E9%252599%2525A9%2525E5%252585%2525AC%2525E5%2525BC%252580%2525E4%2525BF%2525A1%2525E6%252581%2525AF%2525E6%25258A%2525AB%2525E9%25259C%2525B2%2526region%253DBODY%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253D%2525E7%2525AB%252599%2525E5%252586%252585%2525E6%252590%25259C%2525E7%2525B4%2525A2%2525E7%2525BB%252593%2525E6%25259E%25259C%2525E9%2525A1%2525B5%2526pidt%253D1%2526oid%253Dhttp%25253A%25252F%25252Fwww.cpic.com.cn%25252Fir%25252Fgszl%25252Fgsgk%25252F%25253FsubMenu%25253D1%252526inSub%25253D1%252526keywords%25253D%252525E5%25252585%252525AC%252525E5%252525BC%25252580%252525E4%252525BF%252525A1%252525E6%25252581%252525AF%2526ot%253DA',
                  'Host': 'life.cpic.com.cn',
                  'Referer': 'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/?subMenu=1&inSub=3',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                  }
        
      
        zaishou_urls = ['http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/zbcp/sx/',  #寿险
                       'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/zbcp/nj/',  #年金
                       'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/zbcp/ywx/', #意外险
                       'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/zbcp/jkx/', #健康险
                       ] 
        
        for url in zaishou_urls:        
                    yield scrapy.Request(url=url,headers= header ,callback=self.zaishou_parse)
        
            
        tingshou_urls = ['http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/tbcp/sx/',   #寿险
                        'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/tbcp/nj/',   #年金
                        'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/tbcp/ywx/',  #意外险
                        'http://life.cpic.com.cn/xrsbx/gkxxpl/jbxx/gsgk/jydbxcpmljtk/tbcp/jkx/',  #健康险
                       ]
        
        for url in tingshou_urls:       
                   yield scrapy.Request(url=url,headers= header ,callback=self.tingshou_parse)
        
            
    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = re.findall('<a href=(.*)?target(.*)?/a>',response.text)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem()            
                item['company_name'] = '太保人寿'
            
                item['product_type'] = ''
                item['product_id'] = ''
                item['product_name'] = re.findall('>(.*)?<',part[1])[0]
                item['product_sale_status'] = '在售'
                item['product_contract_link'] = "http://life.cpic.com.cn"+ re.sub('"','',part[0])
                item['product_price_link'] = ''
            
                item['product_start_date'] =  ''
                item['product_end_date'] = ''  
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]shtml",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.zaishou_parse)
                   
                
    def tingshou_parse(self, response):                
        # 从每一行抽取数据
        result = re.findall('<a href=(.*)?target(.*)?/a>',response.text)
        for part in result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()            
            item['company_name'] = '太保人寿'
            
            item['product_type'] = ''
            item['product_id'] = ''
            item['product_name'] = re.findall('>(.*)?<',part[1])[0]
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "http://life.cpic.com.cn"+ re.sub('"','',part[0])
            item['product_price_link'] = ''
            
            item['product_start_date'] =  ''
            item['product_end_date'] = ''  
            # 输出数据
            yield item 
        # 找到下一页的代码
        next_pages = re.findall("index_\d+[.]shtml",response.text)
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.tingshou_parse)