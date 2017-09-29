# -*- coding: utf-8 -*-
import sys
sys.path.append('spiders/spiders/')
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())

urlsCurrent= ['https://www.coindesk.com/vivid-history-money-got-free-untold-story-bitcoin/',
              'https://www.coindesk.com/untangling-bitcoin-russell-yanofsky-taking-apart-cryptos-oldest-code/']

process.crawl('https://www.coindesk.com', urls=urlsCurrent)


#urlsCurrent=  ['https://cointelegraph.com/news/gibraltars-financial-regulator-takes-note-of-ico-boom-issues-warning',
#        'https://cointelegraph.com/news/is-blockchain-technology-really-the-answer-to-decentralized-storage',
#        'https://cointelegraph.com/news/cftc-files-first-case-regarding-against-bitcoin-fraudsters']
#process.crawl('https://cointelegraph.com', urls=urlsCurrent)
process.start()

