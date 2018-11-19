# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
import pymongo

class GuokrPipeline(object):
    def open_spider(self,spider):
        self.file = open('guokr.txt','wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

        self.con = pymongo.MongoClient()
        self.database = self.con['guokr']
        self.conllection = self.database['guokr']

    def process_item(self, item, spider):
        self.exporter.export_item(item)

        self.conllection.insert_one(item)

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

        self.con.close()