import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=data&profession_only=1']

    def parse(self, response: HtmlResponse):

        vacancy = response.css(
            'div.f-test-vacancy-item a._6AfZ9::attr(href)'
        ).extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
        pagination = response.css('a[rel="next"]:last-of-type::attr(href)').get()
        if pagination:
            next_page = 'https://russia.superjob.ru' + pagination
            response.follow(next_page, callback=self.parse)
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div.f-test-vacancy-base-info h1::text').get()
        salary = response.css('meta[name="description"]::attr(content)').getall()[0].split('зарплата ')[-1]
        vacancy_link = response.url
        site = self.allowed_domains[0]

        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, site=site)