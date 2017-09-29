# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderCointelegraphExplained(scrapy.Spider):
    name = 'cointelegraph.com/explained/'

    def __init__(self ,*args, **kwargs):
        super(SpiderCointelegraphExplained, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        textParts=response.xpath('//div[@class = "name"]').extract() 
        textParts=textParts+response.xpath('//div[@class = "clearfix content"]').extract()
        text=''
        for part in textParts:
            text=text+unicode(part)
        text=fun.textPreprocessing(text)
        News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == response.url).execute()

