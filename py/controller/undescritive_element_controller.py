import json
import csv
import requests
from bs4 import BeautifulSoup
class UndescritiveElementController:
    def undescriptive_link_finder(self, webpage):
        all_links = []
        r = requests.get(webpage, verify=False)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.findAll('a'):          
            print (link)
            invalid_texts = ["clickhere","click","go","click!","link"]
            undescriptive_link_status = False
            link_text=""   
            link_text = str(link.string).lower()
            link_text = link_text.replace(" ", "")
            
            if link_text in invalid_texts or not link.string:
                undescriptive_link_status = True
            else:
                undescriptive_link_status = False  
            if link.contents:
                for content in link.contents:
                    soup2 = BeautifulSoup(str(content), 'html.parser')
                    if soup2.find('img') or soup2.find('i'):
                        undescriptive_link_status = False
            print(undescriptive_link_status)            
            
            attr = {}
            attr['Page'] = webpage
            attr['Element'] = str(link)
            attr['Undescriptive_link_status'] = undescriptive_link_status
            all_links.append(attr)
        for f in all_links:
            print(json.dumps(f, indent=2))
        return all_links

a = UndescritiveElementController()
a.undescriptive_link_finder('http://localhost/class8_1/sample.html')
