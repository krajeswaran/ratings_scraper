#!/usr/bin/env python
import os
import re
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.mkvcage import MkvcageSpider


try:
    os.remove('out.json')
except OSError:
    pass

process = CrawlerProcess(get_project_settings())
spider = MkvcageSpider()
depth = os.getenv('DEPTH', 10)
omdb_key = os.getenv('OMDB_KEY')
process.crawl(spider, depth=depth, omdb_key=omdb_key)
process.start()


def print_nice(d):
    for k, v in d.iteritems():
        print "{} : {}".format(k.encode('utf-8'), v.encode('utf-8'))


with open('out.json') as f:
    l = []
    for line in f:
        d = json.loads(line)
        if re.search("S[0-9]{2}E[0-9]{2}", d.get("name", "")):
            # print "Skipping tv episode: ", d["name"]
            continue
        l.append(d)

    sortedlist = sorted(l, key=lambda k: int(k['page']))
    for d in sortedlist:
        print_nice(d)
        print '_________________________________________________________'
