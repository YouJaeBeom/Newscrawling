
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


from datetime import datetime
from dateutil.relativedelta import relativedelta

class NewsbotSpider(scrapy.Spider):

    name = 'Newsbot'
    allowed_domains = ['search.naver.com']
    #start_urls = ['https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'.format("코로나")]

    ## start
    def start_requests(self):
        s_date=datetime(2020,11,4)
        for day in range(300):
            ss=day*-1
            self.start_date = s_date + relativedelta(days=ss)
            self.start_date=self.start_date.strftime("%Y.%m.%d")
            print(self.start_date,"~",self.start_date)
            self.url = 'https://search.naver.com/search.naver'
            start_url = self.url + '?where=news&sm=tab_jum&query={}'.format("코로나") + \
                        "&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={}".format(
                            self.start_date) + "&de={}".format(
                self.start_date) + "&docid=&nso=so%3Ar%2Cp%3Afrom20191101to20201104%2Ca%3Aall&mynews=0&refresh_start=0&related=0"

            print("start_url", start_url)
            yield scrapy.Request(start_url, callback=self.parse_url, dont_filter=True)


    ## URL scrap
    def parse_url(self,response):
        ## news list url search
        crawling_url_list = response.xpath(r'//*[@class="list_news"]/li/div[1]/div/div[1]/div/a[2]/@href').extract()
        for url in crawling_url_list:
            ## news parse
            request = scrapy.Request(url,dont_filter=True, callback=self.parse_news_page)
            yield request

        ## next Page
        next_page_url=response.xpath('//*[@id="main_pack"]/div[2]/div/a[2]/@href').extract()[0]
        next_page_url=self.url+str(next_page_url)
        print("next_page_url",next_page_url)
        yield scrapy.Request(next_page_url,dont_filter=True,callback=self.parse_url)

    ## News Scrap
    def parse_news_page(self,response):
        ## News item
        newsitem=NewscrawlingItem()

        # News text pre-processing
        response = response.replace(body=response.body.replace(b'<br>', b''))
        body = response.xpath(r'(//*[ @ id = "articleBodyContents"])').extract()[0]

        ## 특정 태그 삭제
        body = re.sub(r'<div class="vod_area">.*?</div>', '', body, 0, re.I | re.S)
        body = re.sub(r'<strong.*?>.*?</strong>', '', body, 0, re.I|re.S)
        body = re.sub(r'<span.*?>.*?</span>', '', body, 0, re.I|re.S)
        body = re.sub(r'<ul>.*?</ul>', '', body, 0, re.I|re.S)


        ## 의미없는 값제거
        body = body.replace("// flash 오류를 우회하기 위한 함수 추가","")
        body = body.replace("function _flash_removeCallback() {}", "")
        
        ## 태그 삭제
        body = re.sub(r'<.*?>','',body)
        
        ## 문자 공백제거
        body = body.strip()

        ## News date
        newsitem['date'] = response.xpath(r'//*[@id="main_content"]/div[1]/div[3]/div/span[@class="t11"]/text()').extract()[0]

        ## News title
        newsitem['News_title'] = response.xpath(r'//*[@id="articleTitle"]/text()').extract()[0]

        ## News text
        newsitem['News_text'] = body

        ## item export
        yield newsitem










