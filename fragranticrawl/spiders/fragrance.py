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
        'men': 'MEN',
        'women': 'WOMEN',
        'women and men': 'EVERYONE'
    }

    def parse_items(self, response):
        fragrance = Fragrance()
        fragrance['brand'] = response.css(
            '#col1 > div > div > p > span:nth-child(1) > span > a > span'
        ).extract_first()
        name, gender = response.css(
            'h1 span::text').extract_first().split(fragrance['brand'])
        fragrance['name'] = name
        fragrance['perfumers'] = response.css(
            '#col1 > div > div > div:nth-child(7) > p'
        ).xpath('.//a//b/text()').getall()
        fragrance['notes'] = None

        # Needed from brand's page
        # fragrance['releaseYear'] = None
        fragrance['gender'] = self.genderToEnum[gender[4:]]

        return fragrance
