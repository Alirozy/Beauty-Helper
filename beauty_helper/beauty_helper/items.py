# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    website = scrapy.Field()
    type = scrapy.Field()        
    description = scrapy.Field()
    production_year = scrapy.Field()
    poster_url = scrapy.Field()  
    stores_name = scrapy.Field() 
    stores_url = scrapy.Field()  
    price = scrapy.Field()
    currency = scrapy.Field()
    stock = scrapy.Field()    
    rating = scrapy.Field()


    