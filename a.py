#!/usr/bin/env python2
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

    name = "gov"
    allowed_domains = [ "gov.cn" ]
    start_urls = [ "http://www.gov.cn/" ]
    custom_settings = {
            'CONCURRENT_ITEMS': 256,
            'CONCURRENT_REQUESTS': 256,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 256,
            'DEPTH_PRIORITY': -10, # negative means depth first
    }

    # http://doc.scrapy.org/en/latest/topics/link-extractors.html
    rules = (
            Rule(LxmlLinkExtractor(allow=[r'.*\.js'],
                                   tags=['script',],
                                   attrs=['src',],
                                   deny_extensions=(),),
                 callback='parse_blob',
                 follow=False),

            Rule(LxmlLinkExtractor(allow=[r'.*\.css'],
                                   tags=['link',],
                                   attrs=['href',],
                                   deny_extensions=(),),
                 callback='parse_css',
                 follow=False),

            Rule(LxmlLinkExtractor(allow=[r'.*\..*'],
                                   tags=['img',],
                                   attrs=['src',],
                                   # restrict_xpaths='//img',
                                   deny_extensions=(),),
                 callback='parse_blob',
                 follow=False),


            Rule(LxmlLinkExtractor(allow=[r'.*\..*'],
                                   tags=['iframe',],
                                   attrs=['src',],
                                   deny_extensions=(),),
                 callback='parse_html',
                 follow=True),

            Rule(LxmlLinkExtractor(allow=[r'.*\..*']),
                 callback='parse_html',
                 follow=True),

    )

    def parse_blob(self, response):
        self._save(response)


    def parse_html(self, response):
        self._save(response)


    def parse_css(self, response):

        parser = tinycss.make_parser('page3')

        sheet = parser.parse_stylesheet_bytes(response.body)

        for ruleset in sheet.rules:
            # ruleset: div.big, table.nav

            for dec in ruleset.declarations:
                # dec: width: 100px

                for tok in dec.value:
                    # 3 tok: 1px solid #ff0

                    if tok.type == 'URI':
                        full_url = response.urljoin(tok.value)
                        # if self._exist(full_url):
                        #     continue
                        yield scrapy.Request(full_url, callback=self.parse_blob)

        self._save(response)


    def _exist(self, url):

        fn = url.split('//')[1]
        fn = self.base + '/' + fn

        exi = os.path.isfile(fn)
        return exi

    def _save(self, response):

        url = response.url
        url = url.split('?', 1)[0]

        fn = url.split('//')[1]
        fn = self.base + '/' + fn
        dir_path = os.path.dirname(fn)

        try:
            os.makedirs(os.path.dirname(fn))
        except OSError as e:
            pass

        # if os.path.isfile(fn):
        #     # print 'exists:', fn
        #     return True

        with open(fn, 'wb') as f:
            f.write(response.body)

        # print 'saved:', fn
        return True
