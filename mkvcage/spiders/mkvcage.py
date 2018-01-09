import scrapy
import json


class MkvcageSpider(scrapy.Spider):
    name = "mkvcage"
    HREF_XPATH_SELECTOR = '@href'
    TEXT_XPATH_SELECTOR = 'text()'
    MOVIE_TITLES_XPATH_SELECTOR = '//h2/a'
    IMDB_TITLE_XPATH_SELECTOR = '//span/@data-title'
    MAGNET_URL_XPATH_SELECTOR = "//*[contains(@class,'buttn magnet')]"
    TORRENT_URL_XPATH_SELECTOR = "//*[contains(@class,'buttn torrent')]"
    OMDB_TITLE_SEARCH_URI = 'http://www.omdbapi.com/?apikey={}&i={}'
    OMDB_INTERESTING_ATTRS = ['Actors', 'Plot', 'Genre', 'Awards', 'Year', 'Title']
    MKVCAGE_PAGE = 'http://www.mkvcage.com/category/720p/page/%s'

    def start_requests(self):
        depth = int(self.depth)  # self.settings['DEPTH_LIMIT'] / 10
        urls = [self.MKVCAGE_PAGE % i for i in range(1, depth)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for movie in response.xpath(self.MOVIE_TITLES_XPATH_SELECTOR):
            yield scrapy.Request(
                movie.xpath(self.HREF_XPATH_SELECTOR).extract_first(),
                callback=self.get_ratings,
                meta={'name': movie.xpath(self.TEXT_XPATH_SELECTOR).extract_first()})

    def find_movie_details(self, response):
        try:
            res = json.loads(response.body)
            results = {k: res[k] for k in self.OMDB_INTERESTING_ATTRS}
            for d in res['Ratings']:
                i = {}
                i[d['Source']] = d['Value']
                results.update(i)

            results['magnet'] = response.meta.get('magnet', '')
            results['name'] = response.meta.get('name', '')
            yield results
        except (ValueError, IndexError) as e:
            self.logger.debug("OMDB response content: " + response.body)
            self.logger.error("Error hitting OMDB title search: " + str(e))

    def get_ratings(self, response):
        imdb_title = response.xpath(self.IMDB_TITLE_XPATH_SELECTOR).extract_first()
        magnet = response.xpath(self.MAGNET_URL_XPATH_SELECTOR).xpath(self.HREF_XPATH_SELECTOR).extract_first()
        if not magnet:
            magnet = response.xpath(self.TORRENT_URL_XPATH_SELECTOR).xpath(self.HREF_XPATH_SELECTOR).extract_first()

        yield scrapy.Request(
                self.OMDB_TITLE_SEARCH_URI.format(self.omdb_key, imdb_title),
                callback=self.find_movie_details,
                meta={'magnet': magnet, 'name': response.meta.get('name', '')})
