#!/usr/bin/env python
# coding: utf-8

# usage:
#     pip install scrapy
#     pip install tinycss
#     scrapy runspider a.py

import os

import re
import tinycss

import scrapy
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class RoomSpider(CrawlSpider):

    base = './xx'

    name = "emule"
    # allowed_domains = [ "gov.cn" ]
    start_urls = [ "http://cn163.net/archives/23711/" ]
    custom_settings = {
            'CONCURRENT_ITEMS': 256,
            'CONCURRENT_REQUESTS': 256,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 256,
            'DEPTH_PRIORITY': -10, # negative means depth first
    }

    # http://doc.scrapy.org/en/latest/topics/link-extractors.html
    # rules = (

    #         Rule(LxmlLinkExtractor(allow=[r'.*\..*']),
    #              callback='parse_html',
    #              follow=False),

    # )


    def parse(self, response):

        hrefs = response.css("a::attr('href')")
        for href in hrefs:
            url = href.extract()
            if re.match('ed2k.*720.*mkv', url):
                print url
