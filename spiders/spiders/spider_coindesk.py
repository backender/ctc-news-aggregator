# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderCoindesk(scrapy.Spider):
    name = 'coindesk.com'

    def __init__(self ,*args, **kwargs):
        super(SpiderCoindesk, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
            
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        text=response.xpath('//div[@class = "article-content-container noskimwords"]').extract_first() 
        #text processing
        text=fun.textPreprocessing(text)
        text=text.split('function e t r n c a l')[0]
        text=text.split('image via ')[0]
        text=text.split('Image via ')[0]
        text=text.split('via Shutter')[0]
        News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == str(response.url)).execute()