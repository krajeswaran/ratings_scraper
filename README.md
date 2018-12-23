# Ratings Scraper

A small python script to scrape ratings of a movie/show given a name.

PS: Switch to `mkvcage` branch for a realistic/useful scraper which scrapes ~redacted~ARRRR! website and auguments it with ratings/plot/cast from OMDB + IMDB 

## Approach

Looks like there are many ways we can use IMDB for finding ratings of a title/show/movie.

1. IMDB supports datasets via S3 buckets for paid usage: http://www.imdb.com/interfaces/. For obvious reasons, we won't explore this further.
1. [OMDB](http://www.omdbapi.com/) provides reasonable API access to IMDB data. These APIs are ratelimited. Either a paid account with OMDB or using caching[1] and accepting stale ratings might also be a solution. 
1. IMDB uses [microdata](http://schema.org/AggregateRating) in their movie pages - we can use this to reliably scrape ratings instead of techiniques like stylesheet/markup parsing. This approach is explored with this script.

[1] We can use techniques like:
* pre-emptive caching: say load all newly released movies to cache every few hours 
* combine scraping explained in #3 with caching omdb results. If a rating scrape from imdb doesn't match your rating in cache, fetch from omdb API.

Also this script will use title search 'API' from IMDb to find title Id from the given title.

## What could be better?

* Tests
* Use NLP to smartly parse title names?


## Installation

0. Install python2 and pip2 on your system. Clone this repo to say `ratings_scraper` folder
2. [optional] Create a virtualenv an activate it. Eg. 
```bash
cd ratings_scraper
virtualenv venv
source venv/bin/activate
```
2. Install dependencies: `pip install -r requirements.txt`
3. `cd scraper; python scraper.py <title>`
