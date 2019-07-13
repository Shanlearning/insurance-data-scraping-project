# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exporters import CsvItemExporter

class ProjectInsuranceScrapPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    
    def spider_opened(self, spider):
        # 修改此处的文件储存路径
        dir = 'E:/insurance/保险公司数据统计/'
        self.file = open( dir + spider.name+ '.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig')
        self.exporter.start_exporting()
        
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
