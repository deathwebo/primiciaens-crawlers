# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.exceptions import CloseSpider
from urllib.parse import urljoin

now = datetime.now()
today_formatted = now.strftime('%m/%d/%Y')


class ElmexicanoSpider(scrapy.Spider):
    name = 'elmexicano'
    start_urls = ['https://www.el-mexicano.com.mx/estatal/ensenada/']
    base_url = 'https://www.el-mexicano.com.mx/estatal/'

    def parse(self, response):
        headposts = response.css('.col-md-3')
        result = self.parse_post(headposts[0])
        if result:
            yield result
        result = self.parse_post(headposts[1])
        if result:
            yield result
        headpost = response.css('.col-md-6.mb-4')
        result = self.parse_post(headpost)
        if result:
            yield result
        for post in response.css('.media'):
            result = self.parse_post(post, is_head_post=False)
            if not result:
                raise CloseSpider('finished_today')
            yield result

    def parse_post(self, post, is_head_post=True):
        post__meta = post.css('.post__meta .text-primary::text').get()
        if today_formatted in post__meta:
            relative_url = post.css('a::attr(href)').get()
            url = urljoin(self.base_url, relative_url)
            title = post.css('h4 a::text').get() if is_head_post else post.css('h5 a::text').get()
            return {
                "title": title,
                "url": url,
                "website": "el-mexicano.com"
            }
        return False
