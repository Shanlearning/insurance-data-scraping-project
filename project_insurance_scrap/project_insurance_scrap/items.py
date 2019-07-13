# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjectInsuranceScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    
    product_type = scrapy.Field()
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_sale_status = scrapy.Field()
    
    
    product_contract_link = scrapy.Field()
    product_price_link = scrapy.Field()
    
    
    product_start_date = scrapy.Field()
    product_end_date = scrapy.Field()
    
    
    
