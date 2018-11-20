import sys
import json
import os
import requests
import shutil
from bs4 import BeautifulSoup


class WebsiteCloner:
    base_dir = os.getcwd()

    project_path = "../" + "cloned_site"
    os.makedirs(project_path, exist_ok=True)

    visited_links = []
    error_links = []

    def save(self, bs, element, check, site_name):
        links = bs.find_all(element)

        for l in links:
            href = l.get("href")
            if href is not None and href not in WebsiteCloner.visited_links:
                if check in href:
                    href = l.get("href")
                    print("Working with : {}".format(href))
                    if "//" in href:
                        path_s = href.split("/")
                        file_name = ""
                        for i in range(3, len(path_s)):
                            file_name = file_name + "/" + path_s[i]
                    else:
                        file_name = href

                    l = site_name + file_name

                    try:
                        r = requests.get(l, verify=False)
                    except requests.exceptions.ConnectionError:
                        WebsiteCloner.error_links.append(l)
                        continue

                    if r.status_code != 200:
                        WebsiteCloner.error_links.append(l)
                        continue

                    os.makedirs(os.path.dirname(
                        WebsiteCloner.project_path + file_name.split("?")[0]), exist_ok=True)
                    with open(WebsiteCloner.project_path + file_name.split("?")[0], "wb") as f:
                        f.write(r.text.encode('utf-8'))
                        f.close()

                    WebsiteCloner.visited_links.append(l)

    def crawl(self, link, site_name):
        full_list = []
        if "http://" not in link and "https://" not in link and not link.startswith('#'):
            link = site_name + link

        if site_name in link and link not in WebsiteCloner.visited_links and not link.startswith('#'):

            print("Working with : {}".format(link))

            path_s = link.split("/")
            file_name = ""
            for i in range(3, len(path_s)):
                file_name = file_name + "/" + path_s[i]

            if file_name[len(file_name) - 1] != "/":
                file_name = file_name + "/"

            try:
                r = requests.get(link, verify=False)

            except requests.exceptions.ConnectionError:
                print("Connection Error")
                sys.exit(1)

            if r.status_code != 200:
                print("Invalid Response")
                sys.exit(1)
            print(WebsiteCloner.project_path + file_name + "index.html")
            os.makedirs(os.path.dirname(WebsiteCloner.project_path +
                                        file_name.split("?")[0]), exist_ok=True)
            with open(WebsiteCloner.project_path + file_name.split("?")[0] + "index.html", "wb") as f:
                text = r.text.replace(site_name, "cloned_site")
                f.write(text.encode('utf-8'))
                

                f.close()

            WebsiteCloner.visited_links.append(link)

            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all('a'):

                try:
                    WebsiteCloner.crawl(self, link.get("href"), site_name)
                except:
                    WebsiteCloner.error_links.append(link.get("href"))

            # a_list = une.detectUnresElement(r)
            # attr = {}

            # attr['page'] = format(link)
            # attr['smells'] = a_list

            # j = {'result':attr}
            # full_list.append(j)
            # for f in full_list:
            #     print(json.dumps(f, indent=2))
        

    def print_result(self):
        print("Link crawled\n")
        for link in WebsiteCloner.visited_links:
            print("---- {}\n".format(link))

        print("\n\n\nLink error\n")
        for link in  WebsiteCloner.error_links:
            print("---- {}\n".format(link))

cloner = WebsiteCloner()
cloner.crawl("http://www.humansofthakurgaon.org/" +
             "/", "http://www.humansofthakurgaon.org/")
cloner.print_result()             
