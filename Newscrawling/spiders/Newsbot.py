
import re
import json
import logging

import scrapy
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from scrapy.utils.project import get_project_settings

settings = get_project_settings()
from Newscrawling.items import NewscrawlingItem

logger = logging.getLogger(__name__)
import time




class NewsbotSpider(scrapy.Spider):

    name = 'Newsbot'
    allowed_domains = ['search.naver.com']
    start_urls = ['https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format("코로나")]


    def parse(self, response):
        print("@@@@@@@@@@@@@@@@@@")
        str_response = response.xpath(r'//*[@class="list_news"]/li/div[1]/div/div[1]/div/a[2]/@href').extract()
        #str_response = response.xpath(r'//*[@id="sp_nws1"]/div[1]/div/div[1]/div/a[2]/@href').extract()
        print(str_response)
        items = []
        NewsItem = NewscrawlingItem()





