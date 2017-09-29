# -*- coding: utf-8 -*-
import re
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderCointelegraph(scrapy.Spider):
    name = 'cointelegraph.com'

    def __init__(self ,*args, **kwargs):
        super(SpiderCointelegraph, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text=response.xpath('//div[@class = "post-full-text contents"]').extract_first() 
        #text processing
        text=fun.textPreprocessing(text)
        News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == response.url).execute()
