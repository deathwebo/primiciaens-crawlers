# -*- coding: utf-8 -*-
import locale
from datetime import datetime
import scrapy
from scrapy.exceptions import CloseSpider

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

now = datetime.now()
today_formatted = now.strftime('%b %d, %Y')


class RadaSpider(scrapy.Spider):
    name = 'radanoticias'
    start_urls = [
        'https://radanoticias.info/category/generales/',
        'https://radanoticias.info/category/policiaca/',
    ]

    def parse(self, response):
        for post in response.css('.feature-two-column'):
            post_date = post.css('.post-date::text').get().lower()
            if today_formatted != post_date:
                raise CloseSpider('finished_today')
            title_wrapper = post.css('.image-post-title')
            url = title_wrapper.css('a::attr(href)').get()
            title = title_wrapper.css('a::text').get()
            yield {
                "title": title,
                "url": url,
                "website": "radanoticias.info"
            }

        next_page = response.css('.pagination a::attr(href)')[-1].get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

