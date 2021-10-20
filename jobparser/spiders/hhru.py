# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=&st=searchVacancy&text=data-scientist']

    def parse(self, response: HtmlResponse):

        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
        pagination = response.css('a[class="bloko-button"][data-qa="pager-next"]::attr(href)').get()
        if pagination:
            next_page = 'https://spb.hh.ru' + pagination
            response.follow(next_page, callback=self.parse)
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').get()
        salary = ''.join(response.css('span[class="bloko-header-2 bloko-header-2_lite"]::text').getall())
        vacancy_link = response.url.split('?')[0]
        site = self.allowed_domains[0]

        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, site=site)
