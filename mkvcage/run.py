#!/usr/bin/env python
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.mkvcage import MkvcageSpider


def print_nice(d):
    for k, v in d.iteritems():
        print "{} : {}".format(k.encode('utf-8'), v.encode('utf-8'))


process = CrawlerProcess(get_project_settings())
spider = MkvcageSpider()
depth = os.getenv('DEPTH', 10)
omdb_key = os.getenv('OMDB_KEY')
process.crawl(spider, depth=depth, omdb_key=omdb_key)
process.start()


with open('out.json') as f:
    for line in f:
        d = json.loads(line)
        print_nice(d)
        print '_________________________________________________________'
