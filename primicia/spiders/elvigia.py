import locale
from datetime import datetime
import scrapy
from scrapy.exceptions import CloseSpider
from urllib.parse import urljoin

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

now = datetime.now()
today_formatted = now.strftime('%A, %-d de %B de %Y')

class ElVigiaSpider(scrapy.Spider):
    name = 'elvigia'
    start_urls = ['https://elvigia.net/archivo/']

    def parse(self, response):
        subtitulo = response.css('.subtitulo-pagina::text').get()
        if subtitulo != today_formatted:
            raise CloseSpider('finished_today')

        for title in response.css('.listado-noticias>li'):
            relative_url = title.css('a ::attr(href)').get()
            url = urljoin(response.request.url, relative_url)
            yield {
                'title': title.css('a ::text').get(),
                'url': url,
                'website': 'elvigia.net'
            }
