# Bitcoin_KnowledgeGraph
Final project for INF558

## Data Crawl
For NYTIMES crawler, NYTIME [Article Search API](https://developer.nytimes.com/article_search_v2.json) is helpful for crawling articles. Node.js code is implemented to save data. npm will be needed for running code.
```
$ npm install
$ node nytimes_crawl.js
```

## Data Cleaning/Processing

### Country Name
1. For some country name with a comma, e.g. Korea, South, I added nationality name fo allCountryNames.txt manually. (All these countries will be printed out after country_aggregate.py is executed.)

## Reference
1. NLTK: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
2. [Country Name](http://www.ed-u.com/country-names.htm)
3. [Nationality Name](http://www.myenglishpages.com/site_php_files/vocabulary-lesson-countries-nationalities.php)