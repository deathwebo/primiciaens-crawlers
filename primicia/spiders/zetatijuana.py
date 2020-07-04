# -*- coding: utf-8 -*-
import locale
from datetime import datetime
import scrapy
from scrapy.exceptions import CloseSpider

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

now = datetime.now()
today_formatted = now.strftime('%A, %-d %B, %Y')


class ZetatijuanaSpider(scrapy.Spider):
    name = 'zetatijuana'
    start_urls = ['https://zetatijuana.com/category/ensenada/']
    stop_crawling = False

    def parse(self, response):
        for nota in response.css('.nota-cat'):
            url = nota.css('div:nth-child(2)').css('a ::attr(href)').get()
            yield scrapy.Request(url, callback=self.parse_note)

            if self.stop_crawling:
                raise CloseSpider('finished_today')
        
        next_page = response.css('.pager a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        
    def parse_note(self, response):
        label_date = response.css('.label-fecha ::text').get()

        if today_formatted not in label_date:
            self.stop_crawling = True
            return

        title = response.css('h1 ::text').get()
        yield {
            "title": title,
            "url": response.request.url,
            "website": "zetatijuana.com"
        }
