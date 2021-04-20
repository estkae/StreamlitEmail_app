import scrapy
from scrapy.crawler import CrawlerProcess
# define spider
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        print(type(response))
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

process = CrawlerProcess(settings={
    "FEEDS": {
        "emails.json": {"format": "json"},
    },
})
process.crawl(QuotesSpider)
process.start()
