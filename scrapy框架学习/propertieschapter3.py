from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from properties.items import PropertiesItem
import datetime
import urlparse
import socket
import scrapy

class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    # Start on a property page
    def start_requests(self):
        return[
        Request(
            "http://",
            callback=self.parse_welcome)]
    def parse_welcome(self,response):
        return FormRequest.from_response(
            response,
            formdata={"user":"user","pass":"pass"}
        )
    def parse(self,response):
        base_url=""
        js=json.loads(response.body)
        for item in js:
            id=item["id"]
            url=base_url+"property_%06d.html"%id
            yield Request(url,callback=self.parse_item)
    import csv
    with open("todo.csv","rU") as f:
            reader=csv.DictReader(f)
            for line in reader:
                print line
    def parse(self, response):
        """ This function parses a property page.
        @url http://web:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_URL
        @scrapes url project spider server date
        """
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)
        # Load fields using XPath expressions
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''),  
                    float),
                    re='[,.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"]'
                    '[1]/text()',
                    MapCompose(unicode.strip), Join())
        l.add_xpath('address',
                    '//*[@itemtype="http://schema.org/Place"]'
                    '[1]/text()',
                    MapCompose(unicode.strip))
        l.add_xpath('image_URL', '//*[@itemprop="image"]'
                    '[1]/@src', MapCompose(
                    lambda i: urlparse.urljoin(response.url, i)))
        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        return l.load_item()


