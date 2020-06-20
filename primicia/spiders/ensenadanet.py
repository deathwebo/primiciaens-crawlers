import scrapy
import locale
from datetime import datetime
from scrapy.exceptions import CloseSpider
from urllib.parse import urljoin

locale.setlocale(locale.LC_TIME, 'es_ES')

now = datetime.now()
today_formatted = now.strftime('%-d de %B de %Y')
published_note_text = 'Nota publicada el {}'.format(today_formatted)

class EnsenadaNetSpider(scrapy.Spider):
    name = 'ensenadanet'
    start_urls = ['http://www.ensenada.net/noticias/']
    page = 1
    stop_crawling = False

    def parse(self, response):
        for title in response.css('.tituloNota'):
            fecha_nota = title.xpath("./../../span[@class='fechaNota']/text()").get()
            if published_note_text != fecha_nota:
                self.stop_crawling = True
                break
            
            relative_url = title.xpath("./../../a/@href").get()
            url = urljoin(response.request.url, relative_url)
            yield {
                'title': title.css('span ::text').get(),
                'url': url,
                'website': 'ensenada.net'
            }

        if self.stop_crawling:
            raise CloseSpider('finished_today')
        xpath = "//div[@class='pagination']/a[text()='{}']/@href".format(self.page+1)
        next_page = response.xpath(xpath).get()
        if next_page is not None:
            self.page = self.page + 1
            yield response.follow(next_page, callback=self.parse)
