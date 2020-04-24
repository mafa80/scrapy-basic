import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from walt.items import WaltItem


class WaltSpider(CrawlSpider):
    name = 'woody'
    item_count = 0
    allowed_domain = ['https://www.walmart.ca/en']
# podemos ilar mas peticiones compa
    start_urls = ['https://www.walmart.ca/en/grocery/N-117']


# reglas para brincar o hacer cosas chulas
    rules = {
        # Para cada item
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//*[@id="riHzES5"]/div/a')), callback='parse_item', follow=False)

    }

    def parse_item(self, response):
        print('entro a busvar items')
        ml_item = WaltItem()
        # info de producto
        ml_item['nombre'] = response.xpath(
            'normalize-space(//div[@class="title"]').extract()
        ml_item['sku'] = response.xpath(
            '//div[@class="description"]').extract()
        ml_item['precio'] = response.xpath(
            'normalize-space(//span[@class="all-price-sections"])').extract()
        ml_item['review'] = response.xpath(
            'normalize-space(//div[@class="ratings"])').extract()
        self.item_count += 1
        if self.item_count > 10:
            print('entro')
            raise CloseSpider('item_exceeded')
        yield ml_item
