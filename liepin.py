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
    start_urls = [ "https://lpt.liepin.com/soresume/so/" ]
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

    def request(self, url, callback):

        formdata = {
                'pageSize':  '20',
                'contains_wantdq': '1',
                'searchKey': '147426994522522324198',
                'filterKey': '',
                'degrade': 'true',
                'curPage': '',
                'csCreateTimeFlag': '',
                'csCreateTime': '',
                'csId': '',
                'keysRangType': '',
                'keys': '分布式',
                'searchLevel': '',
                'dqs': '010',
                'language_content': '',
                'yearSalarylow': '',
                'yearSalaryhigh': '',
                'wantYearSalaryLow': '',
                'wantYearSalaryHigh': '',
                'workyears': '',
                'age': '',
                'sex': '',
                'updateDate': '',
                'userStatus': '',
                'sortflag': '',
                'pn': '2',
        }

        request = scrapy.http.FormRequest(url=url, callback=callback, formdata=formdata)
        # request.cookies['over18'] = 1

        headers = {
                'Pragma': 'no-cache',
                'Origin': 'https://lpt.liepin.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4,ja;q=0.2,ko;q=0.2,zh-TW;q=0.2',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Referer': 'https://lpt.liepin.com/soresume/so/',
                'Cookie': '__uuid=1474269848427.09; _uuid=4154A3B5FFA8420C295BADBF986A5C40; gr_user_id=dbb0b4e7-d95f-4fe8-8f2e-fac0cd90b0aa; _fecdn_=0; 8955370d=0e12a8e887c9ad22067116170f141bce; verifycode=707b6b06fcfe4c8e8774fe827150e8ad; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1474269854; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1474269902; user_name=%E5%91%A8%E5%A8%9F%E5%A8%9F; user_id=5cff3421ad989bd26f22e79200b1344f; lt_auth=vLsJaCMNmQmv5Hjb3DNYsK5O3NuhA2yd%2FH4KjUtSgtK%2BWKfj4PzgQAmDr7gPxBIhkBwjd8ULNbf6%0D%0AN%2B73wHBJ6ksQwGugiZ%2BxveW80GEBTeBcc6ilgf%2Bqms%2FQS51xlS0Bz3dl9XkbwkT%2Bt0UiZoa%2FmAs%3D%0D%0A; user_kind=1; login_temp=islogin; __nnn_bad_na_=232627b2b4fde820; _e_ld_auth_=9e965b72864699c9; em_username=9285866453v2423243194; em_token=YWMtF0q6iHgjEeatJEMRqXffhAAAAVhOaWJer5xHal1F57yw0nPipEY3wrVXwcI; fe_lpt_phonetest=true; JSESSIONID=D4D28656D823C43C25E20D3C0ECD5A64; __tlog=1474269848429.14%7C00000000%7C00000000%7C00000000%7C00000000; __session_seq=8; __uv_seq=8; _mscid=00000000; b-beta2-config=%7B%22hasPhoneNum%22%3A%220%22%2C%22ecreate_time%22%3A%2220150707%22%2C%22v%22%3A%222%22%2C%22d%22%3A299%2C%22e%22%3A8541048%2C%22ejm%22%3A%221%22%2C%22entry%22%3A%220%22%2C%22p%22%3A%222%22%2C%22n%22%3A%22%E5%91%A8%E5%A8%9F%E5%A8%9F%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A8541048%2C%22jz%22%3A%220%22%2C%22version%22%3A%222%22%7D',
        }


        for k, v in headers.items():
            request.headers[k] = v

        for k in dir(request):
            print k, getattr(request, k)
        return request


    def start_requests(self):
        for i,url in enumerate(self.start_urls):
            yield self.request(url, self.parse_item)

    def parse_item(self, response):

        hrefs = response.css(".list-table .basic .msg a::attr('href')")
        for href in hrefs:
            url = href.extract()
            print url
