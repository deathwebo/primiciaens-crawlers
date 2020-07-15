import locale
from datetime import datetime
import scrapy
from urllib.parse import urljoin

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

now = datetime.now()
today_formatted = now.strftime('%Y-%m-%d')


class ElimparcialSpider(scrapy.Spider):
    name = 'elimparcial'
    start_urls = ['https://www.elimparcial.com/ajax/get_section_news.html?viewmore=%2Fajax%2Fget_section_news.html&page=1&size=30&section=ensenada&publication=3']

    def parse(self, response):
        articles = response.css('article')

        for article in articles:
            article_datetime = article.css('time::attr(datetime)').get()
            if today_formatted not in article_datetime:
                break
            link = article.css('h2 a::attr(href)').get()
            title = article.css('h2 a::text').get()
            url = urljoin("https://www.elimparcial.com", link)
            yield {
                'title': title,
                'url': url,
                'website': 'elimparcial.com'
            }
