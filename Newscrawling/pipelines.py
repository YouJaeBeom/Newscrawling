# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
import time
from scrapy.utils.project import get_project_settings
settings =get_project_settings()
from Newscrawling.utils import mkdirs
from scrapy.exporters import JsonLinesItemExporter
logger = logging.getLogger(__name__)


class NewscrawlingPipeline(object):
    def __init__(self):
        self.myCsv = csv.writer(open('news.csv', 'w',encoding='utf-8-sig',newline=''))
        self.myCsv.writerow(['date', 'News_title','News_text'])

    def process_item(self, item, spider):
        self.myCsv.writerow([item['date'], item['News_title'],item['News_text']])
        return item




