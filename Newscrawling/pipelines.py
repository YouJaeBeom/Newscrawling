# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import time
from scrapy.utils.project import get_project_settings
settings =get_project_settings()
from Newscrawling.utils import mkdirs
from scrapy.exporters import JsonLinesItemExporter
logger = logging.getLogger(__name__)


class NewscrawlingPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonLinesPipeline(object):
    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        # print(spider.name, 'open spider')
        self.name = spider.name
        # print(self.name)
        self.time = spider.start
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveUserPath)

        file = open(f'{self.saveUserPath}/{self.name}.json', 'wb')
        self.files[spider] = file

        self.exporter = JsonLinesItemExporter(file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        # print(spider.name, self.name)
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        logger.warning(f'{self.name} finish {time.time() - self.time}')

    def process_item(self, item, spider):
        # if item['usernameTweet'] == self.name:
        self.exporter.export_item(item)
        return item