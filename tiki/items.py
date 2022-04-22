# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Tiki_Product(scrapy.Item):
    Id = scrapy.Field()
    Name = scrapy.Field()
    Sku = scrapy.Field()
    Current_price = scrapy.Field()
    List_price = scrapy.Field()
    Original_price = scrapy.Field()
    Discount = scrapy.Field()
    Discount_rate = scrapy.Field()
    Rating_average = scrapy.Field()
    Review_count = scrapy.Field()
    Favourite_count = scrapy.Field()
    Inventory_status = scrapy.Field()
    Inventory_type = scrapy.Field()
    Day_ago_created = scrapy.Field()
    All_time_quantity_sold = scrapy.Field()
    Brand = scrapy.Field()
    Current_seller = scrapy.Field()
    Rank = scrapy.Field()
    Other_sellers = scrapy.Field()
    Seller_specifications = scrapy.Field()
    Description = scrapy.Field()