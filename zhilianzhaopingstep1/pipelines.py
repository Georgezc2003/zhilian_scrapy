# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class Zhilianzhaopingstep1Pipeline(object):
    def __init__(self):
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient('localhost', 27017)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        print("DB established")
        self.post.remove()
        # self.post.ensure_index('company_job_name',unique=True)

    def process_item(self, item, spider):
        recruitment_information = dict(item)
        try:
            self.post.insert(recruitment_information)
        except:
            pass
        return item
