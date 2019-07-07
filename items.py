# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectInsuranceScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    product = scrapy.Field()
    status = scrapy.Field()
    contract_link = scrapy.Field()
    price_link = scrapy.Field()
    
