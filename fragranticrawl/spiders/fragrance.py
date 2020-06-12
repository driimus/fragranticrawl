from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fragranticrawl.items import Fragrance


class FragranceSpider(CrawlSpider):
    name = 'fragrance'

    allowed_domains = ['fragrantica.com']
    start_urls = [
        'http://www.fragrantica.com/designers/Lanvin.html',
    ]
    rules = [Rule(LinkExtractor(allow='(/perfume/Lanvin/)((?!:).)*$'),
                  callback='parse_items', follow=True)]

    genderToEnum = {
        'men': 'MASCULINE',
        'women': 'FEMININE',
        'women and men': 'UNISEX'
    }

    def parse_items(self, response):
        fragrance = Fragrance()
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
        fragrance['notes'] = response.css(
            '#col1 > div > div > div:nth-child(13) > div:nth-child(1) > p'
        ).xpath('.//span//img/@alt').getall()

        # Needed from brand's page
        # fragrance['releaseYear'] = None
        fragrance['gender'] = self.genderToEnum[gender]

        return fragrance
