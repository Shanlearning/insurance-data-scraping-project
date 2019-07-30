# -*- coding: utf-8 -*-
import scrapy
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan

class A平安健康Spider(scrapy.Spider):
    name = '平安健康'
    #https://health.pingan.com/

    def start_requests(self):
        urls = ['https://health.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan.shtml'] 
        
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Cookie': 'WEBTRENDS_ID=4.0.4.35-1162819664.30752866; MEDIA_SOURCE_NAME=yl.pingan.com; adms_location=%E5%85%B6%E4%BB%96|0000000000000000$ALL$ALL$ALL; PA_Client_Source=direct; PA_GXH_PD=-1; PA_GXH_NSS=; PA_GXH_WSS=; USER_TRACKING_COOKIE=192.168.204.4-1563781889836.836000000; BIGipServerng_pa18-paweb_DMZCLOUD_PrdPool=3479443884.31614.0000; BIGipServerpa18cms_static_PrdPool=503585964.4983.0000; Hm_lvt_5c327520340e087bbe22ba0399dc4cf0=1563848399; _ga=GA1.2.1815662362.1563848399; _gid=GA1.2.1679710622.1563848399; TOA_CSHI_WLS_HTTP_BRIDGE=E-QcoN-SFfK7Mb6-1p1Y_9ky_DjH0F7MjJfwVhyhWy0XlhrTEEaO!-758099432; BIGipServerEHIS-CSHI_PRDPool=486152620.27006.0000; inner_media=https://health.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan.shtml-%E4%BF%9D%E9%99%A9%E4%BA%A7%E5%93%81%E7%9B%AE%E5%BD%95%E5%8F%8A%E6%9D%A1%E6%AC%BE-%E4%B8%AD-20; Hm_lpvt_5c327520340e087bbe22ba0399dc4cf0=1563849489; WT-FPC=id=4.0.4.35-1162819664.30752866:lv=1563849489211:ss=1563848399829:fs=1563781889215:pn=28:vn=2',  
                  'Host': 'health.pingan.com',
                  'Referer': 'https://health.pingan.com/gongkaixinxipilu/baoxianchanpinmulujitiaokuan_5.shtml',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36}'
                  }
        
        for url in urls:        
            yield scrapy.Request(url=url ,headers= header, callback=self.parse)
            
    def parse(self, response):
        # 从每一行抽取数据
        result = response.css('li').extract()
        result = shan.str_keep('time_r',result)
        for part in result:
                 # 在售保险的内容输入
                item = ProjectInsuranceScrapItem() 
                item['company_name'] = '平安健康'
                name = shan.str_extract('title="(.*?)"',part) 
                if "（停售）" in name:
                    item['product_name'] = shan.str_extract("(.*?)（停",name)
                    item['product_sale_status'] = '停售'
                elif "（自" in name:
                    item['product_name'] = shan.str_extract("(.*?)（自",name)
                    item['product_sale_status'] = '停售'
                else:
                    item['product_name'] = name
                    item['product_sale_status'] = '在售'
                item['product_contract_link'] = shan.str_extract('href="(.*?)">',part)
                # 输出数据
                yield item 
                
        # 找到下一页的代码
        a = response.css('.next').extract()
        next_pages = shan.str_extract('href="(.*?)">',a)
        for next_page in next_pages:
            yield response.follow("https://health.pingan.com" + next_page, callback=self.parse)