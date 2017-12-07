#!/usr/bin/env python

from urllib import urlopen
import sys
import logging
import microdata
import requests
from requests import RequestException
import json


class Scraper(object):
    """
    Class for scraping IMDB ratings using HTML5 microformat
    """

    def __init__(self):
        self.l = logging.getLogger('scraper')
        self.l.setLevel(logging.INFO)
        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.l.addHandler(ch)
        self.given = ''
        self.IMDB_TITLE_SEARCH_URI = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
        self.IMDB_TITLE_URI = 'http://www.imdb.com/title/%s/'

    def find_imdb_titles(self):
        assert self.given != ''
        try:
            r = requests.get(self.IMDB_TITLE_SEARCH_URI % self.given)
            response = json.loads(r.content)
            results = response.get('title_exact', [])
            ids = [x['id'] for x in results]
            names = [x['title'] for x in results]
            return zip(ids, names)
        except (RequestException, IndexError) as e:
            self.l.debug("IMDB response content: " + r)
            self.l.error("Error hitting IMDB title search: " + str(e))

    def find_rating(self, title):
        tt_uri = self.IMDB_TITLE_URI % title
        try:
            page = microdata.get_items(urlopen(tt_uri))
            return page[0].aggregateRating.ratingValue
        except (AttributeError, IndexError) as e:
            self.l.debug("Parsed microdata content: " + str(page))
            self.l.error("Error parsing IMDB microdata: " + str(e))

    def parse_arg(self):
        try:
            self.given = sys.argv[1]
        except IndexError:
            self.l.error('Need to supply a title to search for. \n'
                         'Usage: python scraper.py <title>')
            sys.exit(-1)

    def scrape(self):
        self.parse_arg()

        hits = self.find_imdb_titles()
        if not hits:
            print "Sorry, no results found for: ", self.given
            sys.exit(-1)

        for title in hits:
            print "Title: {} , Rating: {}".format(title[1],
                                                  self.find_rating(title[0]))


if __name__ == "__main__":
    scraper = Scraper()
    try:
        scraper.scrape()
    except KeyboardInterrupt:
        print "Bye!"
