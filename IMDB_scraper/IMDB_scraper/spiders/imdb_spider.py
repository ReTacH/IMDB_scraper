# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt6723592/']
    def parse(self, response):
        # This parse method navigates to the Cast&Crew page
        cast_urls = response.urljoin("fullcredits/")
        yield scrapy.Request(cast_urls, callback = self.parse_full_credits)
    def parse_full_credits(self,response):
        # This parse method navigates to the page of each actors listed on the page
        relative_actor_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        actor_urls = [response.urljoin(a) for a in relative_actor_urls]
        for urls in actor_urls:
            yield scrapy.Request(urls, self.parse_actor_page)
    def parse_actor_page(self,response):
        # This parse method acquires the name of the actor and movie on which he/she worked
        actor_name = response.css("span.itemprop::text")[0].get()
        movie_or_TV_name = response.css("div.filmo-category-section")[0].css("b a::text").getall()
        yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}