import scrapy
from urllib.parse import urljoin

class ElVigiaSpider(scrapy.Spider):
    name = 'elvigia'
    start_urls = ['https://elvigia.net/archivo/']

    def parse(self, response):
        for title in response.css('.listado-noticias>li'):
            relative_url = title.css('a ::attr(href)').get()
            url = urljoin(response.request.url, relative_url)
            yield {
                'title': title.css('a ::text').get(),
                'url': url,
                'website': 'elvigia.net'
            }
