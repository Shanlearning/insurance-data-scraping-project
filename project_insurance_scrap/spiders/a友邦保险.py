# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from project_insurance_scrap.items import ProjectInsuranceScrapItem
import re


class A友邦保险Spider(scrapy.Spider):
    # 抓取机名字
    name = '友邦保险'

    def start_requests(self):
        # 输入在售保险的第一页网址
        zaishou_urls = [
            'https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin/zaishouchanpin.html', ]
        for url in zaishou_urls:
            yield SplashRequest(url = url, callback=self.zaishou_parse)

        # 输入停售保险的第一页网址
        tingshou_urls = [
            'https://www.aia.com.cn/zh-cn/aia/media/gongkaixinxipilou/dongtaichanpin/tingshou.html', ]
        for url in tingshou_urls:
            yield SplashRequest(url=url, callback=self.tingshou_parse)

    def zaishou_parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").extract()
        zs_result = []
        for part in result:
            if "getProduct" in part:
                zs_result.append(part)

        for part in zs_result:
            # 在售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)

            item['company_name'] = '友邦保险'

            item['product_type'] = ''
            item['product_id'] = part[0]
            item['product_name'] = part[1]
            item['product_sale_status'] = '在售'
            item['product_contract_link'] = "https://www.aia.com.cn" + re.findall('href="(.*?)"',part[3])[0]
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item

    def tingshou_parse(self, response):
        # 从每一行抽取数据
        result = response.css("tr").extract()
        ts_result = []
        for part in result:
            if "getProduct" in part:
                ts_result.append(part)

        for part in ts_result:
            # 停售保险的内容输入
            item = ProjectInsuranceScrapItem()
            part = re.findall('<td>(.*?)</td>', part)

            item['company_name'] = '友邦保险'

            item['product_type'] = ''
            item['product_id'] = part[0]
            item['product_name'] = part[1]
            item['product_sale_status'] = '停售'
            #item['product_contract_link'] = "https://www.aia.com.cn" + re.findall('href="(.*?)"',part[3])[0]
            item['product_price_link'] = ''

            item['product_start_date'] = ''
            item['product_end_date'] = ''
            # 输出数据
            yield item
