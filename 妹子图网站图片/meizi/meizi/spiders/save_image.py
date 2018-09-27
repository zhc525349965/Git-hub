# -*- coding: utf-8 -*-
import scrapy
import os

class SaveImageSpider(scrapy.Spider):
    name = 'save_image'
    allowed_domains = ['mm.chinasareview.com']
    with open('./image_url.txt','r') as f :
        start_urls = f.read().split(',')

    if not os.path.exists('../image'):
        os.mkdir('./image')
    else:
        print('文件夹已经存在')

    def parse(self, response):
        name = ((response.url).split('uploads')[1]).lstrip('/').replace('/','-')
        file_path = './image/'+name
        if os.path.exists(file_path):
            print("%s已经存在"%file_path)
        else:
            with open(file_path,'wb') as f:
                f.write(response.body)