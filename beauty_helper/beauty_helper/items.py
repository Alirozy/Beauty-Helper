# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    type = scrapy.Field()        # e.g., "Moisturizer", "Lipstick"
    description = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    production_year = scrapy.Field()
    stores = scrapy.Field()      # List of stores
    poster_url = scrapy.Field()  # Marketing image link
    url = scrapy.Field()         # Source link


    