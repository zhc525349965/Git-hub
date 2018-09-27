# -*- coding: utf-8 -*-
import scrapy
from qiubai.items import QiubaiItem

class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['www.qiushibaike.com']
    host = "https://www.qiushibaike.com"
    start_urls = ['https://www.qiushibaike.com/8hr/page/1/']

    def parse(self, response):
        content_left = response.xpath('//*[@id="content-left"]')
        div_list = content_left.xpath('./div')
        for div in div_list:
            item =  QiubaiItem()
            author_div = div.xpath("./div[@class='author clearfix']")

            author_name = author_div.xpath("./a/h2/text()").extract_first()
            if author_name:
                item['author_name'] = author_name.strip('\n')
            else:
                item['author_name'] = "匿名"

            content = div.xpath("./a/div[@class='content']/span/text()").extract_first()
            if content:
                item['content'] = content.strip('\n')
            else:
                item['content'] = "[图片]"

            content_url = div.xpath("./a[@class='contentHerf']/@href").extract_first()
            content_url = self.host + content_url
            item['content_url'] = content_url

            yield item

        next_page_url = content_left.xpath("./ul[@class='pagination']/li[last()]/a/@href").extract_first()
        next_page_url = self.host + next_page_url

        if next_page_url:
            yield scrapy.Request(next_page_url,callback=self.parse,dont_filter=True)