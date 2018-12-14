import json
import requests
from bs4 import BeautifulSoup
import sys
requests.packages.urllib3.disable_warnings()
class CrawlerManager:
    visited_links = []
    error_links = []
    def reset(self):
        self.visited_links=[]
        self.error_links = []

    def crawl(self, link, site_name):
        temp_link = site_name+'/'
        if "http://" not in link and "https://" not in link and not link.startswith('#'):
            link = site_name + link
        if site_name in link and temp_link!=link and link not in self.visited_links and not link.startswith('#') and len(self.visited_links)<10: 
            #print("Working with : {}".format(link))
            try:
                r = requests.get(link, verify=False)    
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                sys.exit(1)

            if r.status_code != 200:
                print("Invalid Response")
                sys.exit(1)
            
            self.visited_links.append(link)
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.find_all('a'):        
                try:
                    self.crawl(link.get("href"), site_name)
                except:
                    self.error_links.append(link.get("href"))              
 
# test = CrawlerManager()
# test.crawl("http://data.gov.bd" , "http://data.gov.bd") 
# print("Link crawled\n")
# for link in test.visited_links:
#     print("---- {}\n".format(link))

# print("\n\n\nLink error\n")
# for link in test.error_links:
#     print("---- {}\n".format(link))
