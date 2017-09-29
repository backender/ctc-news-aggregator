# -*- coding: utf-8 -*-
import re
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderNewsbtc(scrapy.Spider):
    name = 'newsbtc.com'

    def __init__(self ,*args, **kwargs):
        super(SpiderNewsbtc, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text=response.xpath('//div[@class = "entry-content"]').extract_first() 
        text=text.split('Disclaimer')[0]
        text=text.split('CDATA id15 Content Ad 2 OA_show 15 ')[0]
        #text processing
        text=fun.textPreprocessing(text)

        #only alphabetic
        News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == response.url).execute()

    

