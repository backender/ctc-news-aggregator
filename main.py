import logging
import urllib2
from model import *
from news_crawler import NewsCrawler

logging.getLogger('scrapy').propagate = False
logging.getLogger('peewee').propagate = False

db.get_conn()
db.create_table(News, safe=True)

n = NewsCrawler()
n.parseInformer()
n.parseBitnewz()
process = n.createCrawlerProcess()
process.start()
