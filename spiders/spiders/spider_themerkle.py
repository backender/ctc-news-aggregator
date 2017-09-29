# -*- coding: utf-8 -*-

import re
import scrapy
import sys
sys.path.append('../../')
from model import *
import spider_functions as fun

class SpiderThemerkle(scrapy.Spider):
    name = 'themerkle.com'

    def __init__(self ,*args, **kwargs):
        super(SpiderThemerkle, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('urls')
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        text=response.xpath('//div[@id = "content_box"]').extract_first() 
        try:
            text=text.split('</span></div></div>')[1]
        except:
            print('error merkle')
        text=text.split('<script type="text/javascript">')[0]
        try:
            text=text.replace('freestar.queue.push(function () { googletag.display(\'TheMerkle_728x90_320x50_BTF\'); });','')
        except:
            print('error replacing the merkle')
        #text processing
        text=fun.textPreprocessing(text)
        try:
            text=fun.textPreprocessing(text)
        except:
            print('error processing')
        try:                
            text=text.replace('freestar queue push function googletag display TheMerkle_728x90_320x50_BTF',' ')
        except:
            print('error 2 replacing')
        #only alphabetic
        try:
            News.update(body=text,
                    bitcoinBoolean=fun.aboutBitcoin(text),
                    ethereumBoolean=fun.aboutEthereum(text),finished=True).where(News.link == response.url).execute()
        except:
            print('error storing')
    

