import feedparser
from dateutil import parser
from pytz import timezone
from model import *
import hashlib

db.get_conn()
db.create_table(BitcoinNews, safe=True)

feed = "http://feed.informer.com/digests/I2GGLAVR70/feeder.rss"

d = feedparser.parse(feed)

def hashLink(link):
    hash_object = hashlib.sha256(link)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def decodeText(text):
    text = "".join(i for i in text if ord(i)<128)
    text = text.decode('utf-8', 'ignore').encode('utf-8')
    return text

for post in d.entries:
    ts = parser.parse(post.published).astimezone(timezone('UTC'))
    post = BitcoinNews(timestamp=ts,
                       title=decodeText(post.title),
                       source=post.source['href'],
                       link=post.link,
                       linkHash=hashLink(post.link))
    post.save()
