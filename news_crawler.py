import feedparser
from pytz import timezone
from model import *
import sys
sys.path.append('spiders/spiders/')
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dateutil import parser
import urllib2

class NewsCrawler():

    def decodeText(self, text):
        text = "".join(i for i in text if ord(i)<128)
        text = text.decode('utf-8', 'ignore').encode('utf-8')
        return text

    def hasAvailableSpider(self, source):
        return source in ['coindesk.com',
                         'cointelegraph.com',
                         'cointelegraph.com/explained/',
                         'bitcoinmagazine.com',
                         'livebitcoinnews.com',
                         'newsbtc.com',
                         'themerkle.com',
                         'bitcoinmagazine.com/articles/',
                         'zerohedge.com']

    def fixSource(self, source,link):
        #get rid of http start
        source=source.split('://')[1]
        #get rid of www
        if 'www.' in source:
            source=source.split('www.')[1]
        source=source.split("/")[0]

        #cointelegraph explained has different style
        if('cointelegraph.com/explained/'in link):
            source='cointelegraph.com/explained/'
        if('bitcoinmagazine.com/articles/'in link):
            source='bitcoinmagazine.com/articles/'
        return source

    def createNewsEntry(self, timeStamp, title, source, link, finished = False):
        if not(self.hasAvailableSpider(source)):
            print('No spider: ' + source )
            print(link)
            return None
        try:
            duplicates = News.select().where(News.link == str(link)).get()
        except:
            databaseObject = News(timestamp = timeStamp,
                               title = self.decodeText(title),
                               source = source,
                               link = link,
                               finished = False)
            return databaseObject.save()

    def parseInformer(self, feed = "http://feed.informer.com/digests/I2GGLAVR70/feeder.rss"):
        #Parse feed
        d = feedparser.parse(feed)
        for post in d.entries:
            post.source['href']=self.fixSource(post.source['href'],post.link)
            post.link=post.link.split('#')[0]#fixes some links
            self.createNewsEntry(timeStamp = parser.parse(post.published).astimezone(timezone('UTC')),
                                 title = self.decodeText(post.title),
                                 source = post.source['href'],
                                 link = post.link)

    def parseBitnewz(self, feed = "http://www.bitnewz.net/rss/feed/", count = 50):
    #second feed
        feed = feed + str(count)
        d = feedparser.parse(feed)
        for post in d['entries']:
            #Getting the correct link from rss feed
            url=post['link']
            page =urllib2.urlopen(url)
            data=page.read()
            data=data.split("<a class=\"btn btn-primary\" href=\"")[1]
            #getting the correct source from feed
            post['link']=data.split("\" target=\"")[0]
            #get rid of http start
            post['source']=str(post['link'])
            post['source']=self.fixSource(post['source'],post['link'])
            post['link']=post['link'].split('#')[0]#fixes some links
            self.createNewsEntry(timeStamp = post['published_parsed'],
                                 title = self.decodeText(post['title']),
                                 source = post['source'],
                                 link = post['link'])

    #Init crawler
    def createCrawlerProcess(self):
        articles = list(News.select(News.link, News.source).where(News.finished == False))
        process = CrawlerProcess(get_project_settings())
        #Recrawl unfinished records in the database
        try:
            for article in articles:
                process.crawl(article.source, urls=[article.link])
                print('Crawling article ' + article.link)
        except:
            print('No unfinished news found')

        return process
