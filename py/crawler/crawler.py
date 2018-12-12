import sys
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
visited_links = []
error_links = []

chrome_options = Options()
chrome_options.add_argument("window-size=1366,768")
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(executable_path='./../chromedriver.exe', chrome_options=chrome_options)

link = "https://bangladesh.gov.bd"
driver.get(link)
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, 'html.parser')

def crawl(link, site_name):
    if "http://" not in link and "https://" not in link and not link.startswith('#'):
        link = site_name + link
    if site_name in link and link not in visited_links and not link.startswith('#') and len(visited_links)<10: 
        print("Working with : {}".format(link))
        try:
            r = requests.get(link, verify=False)    
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            sys.exit(1)
        if r.status_code != 200:
            print("Invalid Response")
            sys.exit(1)
        visited_links.append(link)
        soup = BeautifulSoup(r.text, "html.parser")
        print(r.text)
        for link in soup.find_all('a'):        
            try:
                crawl(link.get("href"), site_name)
            except:
                error_links.append(link.get("href"))    

 
crawl("https://bangladesh.gov.bd" , "https://bangladesh.gov.bd")
print("Link crawled\n")
for link in visited_links:
    print("---- {}\n".format(link))

print("\n\n\nLink error\n")
for link in error_links:
    print("---- {}\n".format(link))


