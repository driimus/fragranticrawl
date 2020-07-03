from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from fragranticrawl.items import Fragrance


class FragranceSpider(CrawlSpider):
    name = 'fragrance'

    allowed_domains = ['fragrantica.com']
    start_urls = [
        'http://www.fragrantica.com/designers/Lanvin.html',
    ]
    rules = [Rule(LinkExtractor(allow='(/designers/Lanvin)((?!:).)*$'),
                  callback='parse_start_url', follow=True)]

    layers = ['base', 'mid', 'top']

    genderToEnum = {
        'male': 'MASCULINE',
        'female': 'FEMININE',
        'unisex': 'UNISEX'
    }

    def parse_start_url(self, response):
        # requests = []
        className = 'cell text-left prefumeHbox px1-box-shadow'
        containers = response.xpath(
            f'//div[@class="{className}"]')
        # select ALL frag containers from res
        # for each frag container
        for container in containers:
            #    create new frag object
            fragrance = Fragrance()
            fragrance['name'] = container.xpath(
                './/div[1]/div[3]/h3/a/text()').get()
            fragrance['gender'] = self.genderToEnum[container.xpath(
                './/div[2]/span[1]/text()').get()]
            releaseYear = container.xpath(
                './/div[2]/span[2]/text()').get()
            fragrance['releaseYear'] = int(releaseYear)
            url = response.urljoin(container.xpath(
                './/div[1]/div[3]/h3/a/@href').get())
        #    req with link to frag
            req = Request(url, callback=self.parse_items)
        #    link frag object to req
            req.meta['frag'] = fragrance
            yield req

    def parse_items(self, response):
        fragrance = response.meta['frag']
        fragrance['thumbnail'] = response.css(
            '#mainpicbox > img').xpath('@src').extract_first()
        fragrance['brand'] = brand = response.css(
            '#col1 > div > div > p > span:nth-child(1) > span > a > span::text'
        ).extract_first()
        name, gender = response.css(
            'h1 span::text'
        ).extract_first().split(f' {brand} for ')
        fragrance['name'] = name
        fragrance['perfumers'] = response.css(
            '#col1 > div > div > div:nth-child(7) > p'
        ).xpath('.//a//b/text()').getall()
        # split into top / mid / base
        notes = response.css(
            '#col1 > div > div > div:nth-child(13) > div:nth-child(1) > p'
        )[::-1]
        notes = list(map(self.parse_notes, notes))
        fragrance['notes'] = {}
        for pair in zip(self.layers, notes):
            fragrance['notes'][pair[0]] = pair[1]

        return fragrance

    def parse_notes(self, response):
        return response.xpath('.//span//img/@alt').getall()
