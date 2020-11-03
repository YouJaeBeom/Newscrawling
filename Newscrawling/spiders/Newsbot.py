
import re
import json
import logging
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

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
    #start_urls = ['https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format("코로나")]

    ## start
    def start_requests(self):
        self.url='https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format("코로나")
        yield scrapy.Request(self.url, callback=self.parse_url,dont_filter=True)

    ## URL scrap
    def parse_url(self,response):
        crawling_url_list = response.xpath(r'//*[@class="list_news"]/li/div[1]/div/div[1]/div/a[2]/@href').extract()
        # str_response = response.xpath(r'//*[@id="sp_nws1"]/div[1]/div/div[1]/div/a[2]/@href').extract()
        for url in crawling_url_list:
            print((url))
            request = scrapy.Request(url,dont_filter=True, callback=self.parse_news_page)
            yield request

    ## News Scrap
    def parse_news_page(self,response):
        print("start???")
        print(response.xpath(r'//*[@id="articleTitle"]/text()').extract())





