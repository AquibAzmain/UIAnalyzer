import os
import requests
from urllib.parse import urlparse, urljoin
import crawler as crawler
from bs4 import BeautifulSoup


class CrawlerController():
    def get_scanned_urls(self, website):
        crawler.website = website
        crawler.crawl_site(crawler.website)
        #print(crawler.scanned_urls)
        return crawler.scanned_urls
    

crawlerController = CrawlerController()
print(crawlerController.get_scanned_urls("http://localhost/class8_1/")) 