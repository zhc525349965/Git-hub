# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Guokr.items import GuokrItem

class GuokrSpider(CrawlSpider):
    name = 'guokr'
    allowed_domains = ['guokr.com']
    start_urls = ['https://www.guokr.com/ask/highlight/?page=1']

    rules = (
        Rule(LinkExtractor(allow=r'page='), follow=True),
        Rule(LinkExtractor(allow=r'question'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = GuokrItem()
        item['answer'] = response.css(".answer-txt p::text").extract()
        item['question'] = response.css("#articleTitle::text").extract_first()
        yield item