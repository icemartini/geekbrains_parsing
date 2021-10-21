import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlin.items import LeroyparserItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://spb.leroymerlin.ru/catalogue/{mark}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath('//div[contains(@class, "largeCard")]//a[@data-qa="product-image"]'
                                     '//@href').extract()
        for link in goods_links:
            yield response.follow('https://spb.leroymerlin.ru' + link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        l = ItemLoader(item=LeroyparserItem(), response=response)
        l.add_xpath("name", '//h1[@class="header-2"]//text()')
        l.add_xpath("photos", '//picture[@slot="pictures"]'
                              '//source[@itemprop="image"]/@srcset')
        l.add_xpath("price", '//span[@slot="price"]//text()')
        l.add_xpath("details", '//dl[@class="def-list"]//dt[@class="def-list__term"]//text() | '
                               '//dl[@class="def-list"]//dd[@class="def-list__definition"]//text()')
        yield l.load_item()
