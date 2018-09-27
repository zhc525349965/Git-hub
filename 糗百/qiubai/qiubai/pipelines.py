# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class QiubaiPipeline(object):
    head = True
    def process_item(self, item, spider):
        with open("qiubai.csv",'a',newline="") as csvfile:
            fieldnames = ["author_name","content","content_url"]
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            if self.head:
                writer.writeheader()
                self.head = False
            writer.writerow(item)
        return item