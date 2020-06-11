from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from fragranticrawl.items import Fragrance


class FragranceSpider(CrawlSpider):
    name = 'fragrance'

    allowed_domains = ['fragrantica.com']
    start_urls = [
        'http://www.fragrantica.com/designers/Lanvin.html',
    ]
    rules = Rule(LinkExtractor(allow='(/perfume/Lanvin/)((?!:).)*$'),
                 callback='parse_items', follow=True)

    def parse_items(self, response):
        fragrance = Fragrance()
        fragrance['name'] = response.css('h1 span::text').extract_first()
        return fragrance
