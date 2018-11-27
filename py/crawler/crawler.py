import sys
import json
import requests
from bs4 import BeautifulSoup

visited_links = []
error_links = []

def crawl(link, site_name):
    full_list=[]
    if "http://" not in link and "https://" not in link and not link.startswith('#'):
        link = site_name + link

    if site_name in link and link not in visited_links and not link.startswith('#') and len(visited_links)<20:
        
        print("Working with : {}".format(link))

        try:
            r = requests.get(link)
            
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            sys.exit(1)

        if r.status_code != 200:
            print("Invalid Response")
            sys.exit(1)
        

        visited_links.append(link)

        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find_all('a'):
                
            try:
                crawl(link.get("href"), site_name)
            except:
                error_links.append(link.get("href"))    

 
crawl("https://bangladesh.gov.bd/site/view/events" , "https://bangladesh.gov.bd/site/view/events")
print("Link crawled\n")
for link in visited_links:
    print("---- {}\n".format(link))

print("\n\n\nLink error\n")
for link in error_links:
    print("---- {}\n".format(link))
