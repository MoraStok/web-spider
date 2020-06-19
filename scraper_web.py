# -*- coding: utf-8 -*-
import scrapy


class ScraperWebSpider(scrapy.Spider):
    name = 'scraper_web'
    allowed_domains = ['https://www.google.com/']
    start_urls = ['http://https://www.google.com//']

    def parse(self, response):
        pass
