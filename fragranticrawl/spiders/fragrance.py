import scrapy
class FragranceSpider(scrapy.Spider):
	name='fragrance'

	def start_requests(self):
		urls = [
		'http://www.fragrantica.com/perfume/Lanvin/Avant-Garde-13612.html',
		]
		return [scrapy.Request(url=url, callback=self.parse)
		for url in urls]

	def parse(self, response):
		url = response.url
		title = response.css('h1 span::text').extract_first()
		print('URL is: {}'.format(url))
		print('Title is: {}'.format(title))
