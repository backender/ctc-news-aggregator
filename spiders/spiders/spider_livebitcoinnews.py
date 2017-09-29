# -*- coding: utf-8 -*-
import re
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderLivebitcoinnews(scrapy.Spider):
    name = 'livebitcoinnews.com'

    def __init__(self ,*args, **kwargs):
        super(SpiderLivebitcoinnews, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text=response.xpath('//div[@class = "post-info"]').extract_first()
        try:
            text=text.split('<!--Content Ad -->')[2]
        except:
            try: 
                text=text.split('<li class="sm-share reddit">')[1]
            except:
                print('error livebitcoinnews')
        text=text.split('<footer class=')[0]
        text=text.split('Header image')[0]
        #text processing
        text=fun.textPreprocessing(text)
        #only alphabetic
        News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == response.url).execute()

    

