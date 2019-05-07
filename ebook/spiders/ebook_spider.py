import scrapy
import re
from ..items import EbookItem
from scrapy.http import Request
import pdb

class EbookSpider(scrapy.Spider):
    name = "ebook"
    allowed_domains = ["qisuu.la"]
    start_urls = [
        "https://www.qisuu.la",
    ]

    def parse(self, response):
        count = 30000
        while count < 40000:
            count+=1
            link = 'https://www.qisuu.la/Shtml' + str(count).zfill(5)+'.html'
            yield Request(url=link,callback=self.ebook)


    def ebook(self, response):
        strurl = response.xpath("//li//script").extract()[0]
        url = re.search(r'https.*txt',strurl).group()
        title = response.xpath("//h1/text()").extract()[0]
        img = "https://www.qisuu.la"+response.xpath("//img/@src").extract()[1]
        author = response.xpath('//li[@class="small"]/text()').extract()[5][5:]
        btype = response.xpath('//div[@class="wrap position"]//a/text()').extract()[2]
        brief = response.xpath('//p/text()').extract()[0]
        item = EbookItem()
        item['url'] = url
        item['img'] = img
        item['author'] = author
        item['title'] = title
        item['btype'] = btype
        item['brief'] = brief
        yield item
