import peewee as pw
import os

db = (pw.MySQLDatabase(
            os.environ['CTC_NEWS_DB'],
            host=os.environ['CTC_NEWS_HOST'],
            port=int(os.environ['CTC_NEWS_PORT']),
            user=os.environ['CTC_NEWS_USER'],
            passwd=os.environ['CTC_NEWS_PASSWORD']))

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class BitcoinNews(MySQLModel):
    timestamp = pw.DateTimeField(null=True)
    title = pw.TextField(null=True)
    source = pw.TextField(null=True)
    link = pw.TextField(null=True)
    linkHash = pw.CharField(primary_key=True)
    class Meta:
        db_table = 'BitcoinNews'
