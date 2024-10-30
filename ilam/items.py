# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst,MapCompose

def text_strip(value):
    return value.strip()

def text_upper(value):
    return value.upper()

# class IlamItem(scrapy.Item):
#     name = scrapy.Field(input_processor=MapCompose(remove_tags ,text_strip ,text_upper) , output_processors=TakeFirst())
#     capital = scrapy.Field(input_processor=MapCompose(remove_tags ,text_strip ,text_upper) , output_processors=TakeFirst())
#     population = scrapy.Field(output_processors=TakeFirst())




class IlamItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_tags ,text_strip ,text_upper) , output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags ,text_strip))
    org_price = scrapy.Field(input_processor=MapCompose(remove_tags ,text_strip))
    available = scrapy.Field()
    img_url = scrapy.Field()
    gallery_url = scrapy.Field()
    caption = scrapy.Field()
    page_url = scrapy.Field(input_processor=MapCompose(remove_tags))
    warranty = scrapy.Field(input_processor=MapCompose(remove_tags))
    register = scrapy.Field(input_processor=MapCompose(remove_tags))
    show_a = scrapy.Field()
