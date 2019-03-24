import scrapy
from scrapy.loader import ItemLoader
from cl.items import CarItem
from itertools import islice


class CarSpider(scrapy.Spider):
  name = "cars"
  start_urls = [
      "https://seattle.craigslist.org/search/cto?postedToday=1&search_distance=20&postal=98052&max_price=5000&auto_make_model=toyota&auto_title_status=1",
      "https://seattle.craigslist.org/search/cto?postedToday=1&search_distance=20&postal=98052&max_price=5000&auto_make_model=honda&auto_title_status=1"
  ]

  def parse(self, response):
    item_links_xpath = "//a[@class='result-title hdrlnk']/@href"
    for sel in response.xpath(item_links_xpath).getall():
      self.logger.info("Find item link: %s", sel)
      yield scrapy.Request(url=sel, callback=self.parse_detail)

  def parse_detail(self, response):
    loader = ItemLoader(item=CarItem(), response=response)
    loader.add_xpath(
        "title",
        "//h2[@class='postingtitle']//span[@id='titletextonly']/text()")
    loader.add_xpath(
        "price", "//h2[@class='postingtitle']//span[@class='price']/text()")
    loader.add_xpath("detail", "string(//section[@id='postingbody'])")
    attributes = response.css('div.mapAndAttrs').xpath(
        ".//p[@class='attrgroup'][2]/span").css("::text").getall()
    keys = islice(attributes, 0, None, 2)
    values = islice(attributes, 1, None, 2)
    pairs = [''.join(t) for t in zip(keys, values)]
    attribute = "|".join(pairs)
    loader.add_value("attribs", attribute)
    postedtime = response.css(
        "p.postinginfo.reveal>time.date.timeago::text").get()
    loader.add_value("posted", postedtime.strip())
    postinfo = response.css("div.postinginfos").xpath(
        "./p[contains(text(), 'post id')]/text()").get()
    loader.add_value("postid", postinfo)
    yield loader.load_item()
