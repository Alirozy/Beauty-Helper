import scrapy
from beauty_helper.items import ProductItem

class BeautySpider(scrapy.Spider):
    name = "beauty_bot"
    
    # You can add many websites here
    start_urls = [
        'https://www.example-beauty-store.com/skincare',
        'https://www.another-health-site.com/new-products'
    ]

    def parse(self, response):
        for product in response.css('div.product-item'):
            item = ProductItem()
            
            # Extracting data using CSS Selectors
            item['name'] = product.css('h2.title::text').get()
            item['price'] = product.css('span.amount::text').get()
            item['rating'] = product.css('div.stars::attr(data-score)').get()
            item['poster_url'] = product.css('img::attr(src)').get()
            
            yield item

        # Logic to follow "Next Page" buttons
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)