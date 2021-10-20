# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt6723592/']
    def parse(self, response):
        cast_urls = response.urljoin("fullcredits/")
        yield scrapy.Request(cast_urls, callback = self.parse_full_credits)
    def parse_full_credits(self,response):
        relative_actor_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        actor_urls = [response.urljoin(a) for a in relative_actor_urls]
        for urls in actor_urls:
            yield scrapy.Request(urls, self.parse_actor_page)
    def parse_actor_page(self,response):