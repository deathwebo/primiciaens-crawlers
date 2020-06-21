# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exceptions import DropItem
import dataset
from datetime import datetime

class PrimiciaPipeline:
    def process_item(self, item, spider):
        return item

class DatabasePipeline:
    def open_spider(self, spider):
        DB_URI = 'postgresql://primicia:primiciapassword!@0.0.0.0:5432/primicia'
        self.db = dataset.connect(os.getenv("DATABASE_URL"), DB_URI)

    def process_item(self, item, spider):
        table = self.db['news']
        now = datetime.now()
        table.insert_ignore(dict(
            url=item['url'],
            title=item['title'],
            website=item['website'],
            dateAdded=now.strftime("%Y-%m-%d"),
            datetimeAdded=now,
            visits=0,
        ), ['url'])
        return item