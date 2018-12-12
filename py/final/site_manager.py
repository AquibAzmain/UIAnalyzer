import requests
import final.crawler_manager as crawler_manager

class SiteManager:

    def verify_site(self, site):
        if "http://" not in site and "https://" not in site and not site.startswith('#'):
            site = "http://"+site
        try:
            r = requests.get(site, verify=False)
        except requests.exceptions.ConnectionError:
            return False   
        if r.status_code != 200:
            return False
        else:
             return True    

    def get_links(self, site):
        print("hello")
        print(site)
        CrawlerManager = crawler_manager.CrawlerManager()
        CrawlerManager.crawl(site , site)
        return CrawlerManager.visited_links

# SiteManager = SiteManager()
# SiteManager.get_links("https://bangladesh.gov.bd")             