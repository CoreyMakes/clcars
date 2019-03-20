# -*- coding: utf-8 -*-
from scrapy.loader.processors import MapCompose, TakeFirst
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re


def remove_dollar_sign(price: str):
  return price.lstrip('$')


def normalise_detail(text):
  text = text.strip()
  text = re.sub(r"\n{2,}", "\n", text)    # strip redundant newlines
  text = re.sub(r" {2,}", " ", text)    # remove redundant spaces
  return text


def extract_number(text):
  m = re.search(r"\d+", text)
  return m.group(0)


class CarItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  title = scrapy.Field(output_processor=TakeFirst())
  price = scrapy.Field(
      input_processor=MapCompose(remove_dollar_sign),
      output_processor=TakeFirst())
  detail = scrapy.Field(
      input_processor=MapCompose(normalise_detail),
      output_processor=TakeFirst())
  attribs = scrapy.Field(output_processor=TakeFirst())
  postid = scrapy.Field(
      input_processor=MapCompose(extract_number), output_processor=TakeFirst())
  posted = scrapy.Field(output_processor=TakeFirst())
  contact = scrapy.Field()
