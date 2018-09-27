# -*- coding: utf-8 -*-
import scrapy

class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['www.meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']

    def parse(self, response):
        detail_url = response.css('.pic a::attr(href)').extract()
        for url in detail_url:
            yield scrapy.Request(url,callback=self.parse_meinv)

        next = response.xpath('//*[@id="wp_page_numbers"]/ul/li/a[contains(text(), "下一页")]/@href').extract_first()
        if next:
            next_url = "http://www.meizitu.com/a/" + next
            yield scrapy.Request(next_url,callback=self.parse)
        else:
            pass

    def parse_meinv(self,response):
        with open('./image_url.txt','a') as f :
            image_urls = response.css('.postContent p img::attr(src)').extract()
            for image_url in image_urls:
                f.write(image_url+',')