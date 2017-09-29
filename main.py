import feedparser
from pytz import timezone
from model import *
import sys
sys.path.append('spiders/spiders/')
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dateutil import parser
import logging 
import urllib2


logging.getLogger('scrapy').propagate = False
logging.getLogger('peewee').propagate = False

db.get_conn()
db.create_table(News, safe=True)
#Init crawler
process = CrawlerProcess(get_project_settings())

#Recrawl unfinished records in the database 
try:
    lastID=0
    while True:
        un=News.select(News.id,News.link, News.source).where( News.id>lastID, News.finished == False).get()
        lastID=un.id
        process.crawl(un.source, urls=[un.link])
        print('Recrawling the news with id '+ str(lastID)+' | '+un.source+' | '+un.link)
except:
    print('No unfinished news found anymore')

#Parse feed
feed = "http://feed.informer.com/digests/I2GGLAVR70/feeder.rss"
d = feedparser.parse(feed)

def decodeText(text):
    text = "".join(i for i in text if ord(i)<128)
    text = text.decode('utf-8', 'ignore').encode('utf-8')
    return text
def hasAvailableSpider(source):
    spiders=['coindesk.com',
             'cointelegraph.com',
             'cointelegraph.com/explained/',
             'bitcoinmagazine.com',
             'livebitcoinnews.com',
             'newsbtc.com',
             'themerkle.com',
             'bitcoinmagazine.com/articles/',
             'zerohedge.com']
    if source in spiders:
        return True
    else: 
        return False
def fixSource(source,link):
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

for post in d.entries:
    post.source['href']=fixSource(post.source['href'],post.link)
    post.link=post.link.split('#')[0]#fixes some links 
    try:
        duplicates = News.select().where(News.link == post.link).get()
    except:
        if(hasAvailableSpider(post.source['href'])):
            ts = parser.parse(post.published).astimezone(timezone('UTC'))
            databaseObject = News(timestamp=ts,
                               title=decodeText(post.title),
                               source=post.source['href'],
                               link=post.link,
                               finished=False)
            databaseObject.save()
            process.crawl(post.source['href'], urls=[str(post.link)])
        else:
            print('No spider: ' + post.source['href'] )
            print(post.link)

#second feed            
feedsToConsider=100
feed = "http://www.bitnewz.net/rss/feed/"+str(feedsToConsider)
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
    post['source']=fixSource(post['source'],post['link'])
    post['link']=post['link'].split('#')[0]#fixes some links 
    try:
        duplicates = News.select().where(News.link == str(post['link'])).get()
    except:
        if(hasAvailableSpider(post['source'])):
            ts = post['published_parsed']
            databaseObject = News(timestamp=ts,
                               title=decodeText(post['title']),
                               source=post['source'],
                               link=post['link'])
            databaseObject.save()
            process.crawl(post['source'], urls=[str(post['link'])])
        else:
            print('No spider: ' + post['source'] )
            print(post['link'])


process.start()   

