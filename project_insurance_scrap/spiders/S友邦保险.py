# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import project_insurance_scrap.scrap_functions as shan
import re

lua = '''  #自定义lua脚本
    function main(splash)
        assert(splash:go(splash.args.url))                                                                            
        assert(splash:wait(10))
        return splash:html()
        end
    '''

class A友邦保险Spider(scrapy.Spider):
    # 抓取机名字
    name = '友邦保险'

    # https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin/tingshou.html
    def start_requests(self):

        # 输入停售保险的第一页网址
        tingshou_urls = [
            'https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin/tingshou.html', ]

        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Encoding: ': 'gzip, deflate, br',
                  'Accept-Language': 'en-US,en;q=0.9',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Cookie': 'Hm_lvt_d0d4f5b1cefb49ac3c9a2777448fe6eb=1562853855,1563004306,1563012996,1563063176; Hm_lpvt_d0d4f5b1cefb49ac3c9a2777448fe6eb=1563071417; _ga=GA1.3.72710742.1562570345; _gid=GA1.3.978365437.1563004305; _sdsat_landing_page=https://www.aia.com.cn/zh-cn/index.html|1563063175358; _sdsat_session_count=7; AMCVS_E10E525A5481ADEC0A4C98C6%40AdobeOrg=1; _sdsat_traffic_source=https://www.aia.com.cn/zh-cn/index.html; _sdsat_lt_pages_viewed=33; _sdsat_pages_viewed=7; AMCV_E10E525A5481ADEC0A4C98C6%40AdobeOrg=-1712354808%7CMCIDTS%7C18091%7CMCMID%7C54112688767367594790453752039430443344%7CMCAAMLH-1563676217%7C11%7CMCAAMB-1563676217%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1563078618s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0',
                  'Host': 'www.aia.com.cn',
                  'If-Modified-Since' : 'Fri, 12 Jul 2019 09:34:46 GMT',
                  'If-None-Match' : '1e36b-58d789ef78fd3-gzip' ,
                  'Referer' : 'https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin.html',
                  'Upgrade-Insecure-Requests' : '1',
                  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                  }

        for url in tingshou_urls:
            yield SplashRequest(url=url, headers= header , args={'lua_source': lua, 'timeout': 3600}, callback=self.tingshou_parse)

            # 输入在售保险的第一页网址
        zaishou_urls = [
            'https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin/zaishouchanpin.html', ]
        for url in zaishou_urls:
             yield SplashRequest(url=url, callback=self.zaishou_parse)

    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").extract()
        zs_result = shan.str_keep("getProduct",result)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)

            item['company_name'] = '友邦保险'

            item['product_id'] = part[0]
            item['product_name'] = part[1]
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "https://www.aia.com.cn" + shan.str_extract('href="(.*?)"',part[3])

            # 输出数据
            yield item

    def tingshou_parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").extract()
        ts_result = shan.str_keep("getProduct",result)

        for part in ts_result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)

            item['company_name'] = '友邦保险'

            item['product_id'] = part[0]
            item['product_name'] = part[1]
            item['product_sale_status'] = '停售'
            item['product_contract_link'] = "https://www.aia.com.cn" + shan.str_extract('href="(.*?)"',part[3])

            # 输出数据
            yield item
