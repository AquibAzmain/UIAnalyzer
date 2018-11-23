import sys
import json
import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from anchor_tag_controller import AnchorTagController
from flash_scroll_controller import FlashScrollController

class CrawlerController:
    visited_links = []
    error_links = []

    # def save(self, bs, element, check, site_name):
    #     links = bs.find_all(element)

    #     for l in links:
    #         href = l.get("href")
    #         if href is not None and href not in CrawlerController.visited_links:
    #             if check in href:
    #                 href = l.get("href")
    #                 print("Working with : {}".format(href))
    #                 if "//" in href:
    #                     path_s = href.split("/")
    #                     file_name = ""
    #                     for i in range(3, len(path_s)):
    #                         file_name = file_name + "/" + path_s[i]
    #                 else:
    #                     file_name = href

    #                 l = site_name + file_name

    #                 try:
    #                     r = requests.get(l, verify=False)
    #                 except requests.exceptions.ConnectionError:
    #                     CrawlerController.error_links.append(l)
    #                     continue

    #                 if r.status_code != 200:
    #                     CrawlerController.error_links.append(l)
    #                     continue

    #                 CrawlerController.visited_links.append(l)

    def crawl(self, link, site_name):
        full_list = []
        if "http://" not in link and "https://" not in link and not link.startswith('#'):
            link = site_name + link

        if site_name in link and link not in CrawlerController.visited_links and not link.startswith('#') and len(CrawlerController.visited_links)<15 and len(CrawlerController.error_links)<20:
            print("Working with : {}".format(link))

            try:
                r = requests.get(link, verify=False)
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                sys.exit(1)

            if r.status_code != 200:
                print("Invalid Response")
                sys.exit(1)

            CrawlerController.visited_links.append(link)

            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all('a'):

                try:
                    CrawlerController.crawl(self, link.get("href"), site_name)
                except:
                    CrawlerController.error_links.append(link.get("href"))

            # a_list = une.detectUnresElement(r)
            # attr = {}

            # attr['page'] = format(link)
            # attr['smells'] = a_list

            # j = {'result':attr}
            # full_list.append(j)
            # for f in full_list:
            #     print(json.dumps(f, indent=2))
        

    def generate_result(self):
        merged_anchor_list = []
        merged_height_list = []
        anchorTagController = AnchorTagController()
        flashScrollController = FlashScrollController()
        driver = flashScrollController.initiate_chrome_driver()

        for link in CrawlerController.visited_links:
            #anchorTag
            anchor_list = anchorTagController.create_json(link)
            merged_anchor_list+=anchor_list
            #flashNavigation
            height_list = flashScrollController.create_json(driver, link)
            merged_height_list+=height_list
                 
        anchorTagController.create_csv(merged_anchor_list)
        flashScrollController.create_csv(merged_height_list)
        # print("\n\n\nLink error\n")
        # for link in  CrawlerController.error_links:
        #     print("---- {}\n".format(link))

cloner = CrawlerController()
cloner.crawl("http://data.gov.bd/", "http://data.gov.bd/")
print(cloner.visited_links)
cloner.generate_result()             
