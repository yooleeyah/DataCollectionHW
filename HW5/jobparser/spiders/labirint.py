import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/научно-популярная/"]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response:HtmlResponse):
        author_w_title = response.xpath("//h1/text()").get().split(': ')
        author = author_w_title[0]
        title = author_w_title[1]
        availability = response.xpath("//div[contains(@class, 'prodtitle-availibility')]//span/text()").get()
        eng_title = response.xpath("//h2[@class='h2_eng']/text()").get()
        genre = response.xpath("//span[contains(@class, 'thermo-item_last')]//span/text()").get()
        age = response.xpath("//div[@id='age_dopusk']/text()").get().replace(' ', '')
        translator = response.xpath("//a[@data-event-label='translator']/text()").getall()
        publisher = response.xpath("//a[@data-event-label='publisher']/text()").get()
        year = int(response.xpath("//div[@class='publisher']/text()").getall()[-1].split(' ')[1])
        _id = int(response.xpath("//div[@class='articul']/text()").get().split(' ')[-1])
        url = response.url
        yield JobparserItem(author=author, title=title, availability=availability,
                            eng_title=eng_title, genre=genre, age=age, translator=translator, publisher=publisher,
                            year=year, _id=_id, url=url)