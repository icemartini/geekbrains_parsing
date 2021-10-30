import scrapy
from itemloaders.processors import TakeFirst, Compose, Identity


def clean_item(items):
    return [item.replace(' ', '') for item in items]


def zip_items(items):
    items = [item.strip() for item in items]
    return dict(zip(items[::2], items[1::2]))


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(output_processor=Identity())
    price = scrapy.Field(input_processor=Compose(clean_item), output_processor=TakeFirst())
    details = scrapy.Field(input_processor=Compose(zip_items))
    pass
