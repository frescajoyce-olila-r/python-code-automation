import scrapy


class DanskindustriDkSpider(scrapy.Spider):
    name = 'danskindustri_dk'
    allowed_domains = ['https://www.danskindustri.dk']
    start_urls = ['http://https://www.danskindustri.dk/']

    def parse(self, response):
        pass
