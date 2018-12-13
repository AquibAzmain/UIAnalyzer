import json
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
class CrawlerManager:
    visited_links = []
    error_links = []
    def reset(self):
        self.visited_links=[]
    def crawl(self, link, site_name):
        if "http://" not in link and "https://" not in link and not link.startswith('#'):
            link = site_name + link
        if site_name in link and link not in self.visited_links and not link.startswith('#') and len(self.visited_links)<20: 
            #print("Working with : {}".format(link))
            try:
                r = requests.get(link, verify=False)    
            except requests.exceptions.ConnectionError:
                print("Connection Error")
            if r.status_code != 200:
                print("Invalid Response")
            
            self.visited_links.append(link)
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.find_all('a'):        
                try:
                    self.crawl(link.get("href"), site_name)
                except:
                    self.error_links.append(link.get("href"))              
 
 
#crawl("https://bangladesh.gov.bd/site/view/events" , "https://bangladesh.gov.bd/site/view/events")
# print("Link crawled\n")
# for link in visited_links:
#     print("---- {}\n".format(link))

# print("\n\n\nLink error\n")
# for link in error_links:
#     print("---- {}\n".format(link))
