# -*- coding: utf-8 -*-
import time
from urllib import parse

import scrapy
from lxml import etree
from scrapy import  Request

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?rh=n%3A283155%2Cn%3A%211000%2Cn%3A5&page=2&language=zh&qid=1595090896&ref=lp_5_pg_2']

    def parse(self, response):
        time.sleep(2)
        titles=response.xpath('//div[@class="sg-col-inner"]/div/h2//a[@class="a-link-normal a-text-normal"]/span/text()').extract()
        price =response.xpath('//div[@class="sg-col-inner"]//div[@class="a-row"]//span[@class="a-price"]/span[@class="a-offscreen"]/text()').extract()
        mark = response.xpath('//div[@class="sg-col-inner"]//div[@class="a-row a-size-small"]/span/a[@class="a-link-normal"]/span/text()').extract()
        print(mark)
        url_1 = 'https://www.amazon.com'
        url_2= response.xpath('//div[@class="sg-col-inner"]/div/h2/a/@href').extract()
        herf = [parse.urljoin(url_1,item) for item in url_2]
        
        for item in zip(titles,herf,price,mark):
            yield {
                "title":item[0],
                "herf":item[1],
                "price":item[2],
                "mark":item[3]
           }
        page_url_1 = 'https://www.amazon.com'
        page_url_2 =response.xpath('//div[@class="a-text-center"]/ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').extract_first()
        next_url = parse.urljoin(page_url_1, page_url_2)
        
        yield Request(next_url)
