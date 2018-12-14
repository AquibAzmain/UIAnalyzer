import json
import csv
import requests
from bs4 import BeautifulSoup
class UndescritiveElementController:
    def undescriptive_element_finder(self, webpage):
        all_elements = []
        r = requests.get(webpage, verify=False)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        button_anchor = soup.find_all('a') + soup.find_all('button')
        for element in button_anchor:          
            invalid_texts = ["clickhere","click","go","click!","link"]
            undescriptive_element_status = False
            element_text=""   
            element_text = str(element.string).lower()
            element_text = element_text.replace(" ", "")
            
            if element_text in invalid_texts or not element.string:
                undescriptive_element_status = True
            else:
                undescriptive_element_status = False  
            if element.contents:
                for content in element.contents:
                    soup2 = BeautifulSoup(str(content), 'html.parser')
                    if soup2.find('img') or soup2.find('i'):
                        undescriptive_element_status = False           
            
            attr = {}
            attr['Page'] = webpage
            attr['Element'] = str(element)
            attr['Undescriptive_status'] = undescriptive_element_status
            all_elements.append(attr)
        for f in all_elements:
            print(json.dumps(f, indent=2))

    
    # def undescriptive_button_finder(self, webpage):
    #     all_elements = []
    #     r = requests.get(webpage, verify=False)
    #     html_doc = r.text
    #     soup = BeautifulSoup(html_doc, 'html.parser')
    #     for element in soup.findAll('button'):          
    #         print (element)
    #         invalid_texts = ["clickhere","click","go","click!","element"]
    #         undescriptive_element_status = False
    #         element_text=""   
    #         element_text = str(element.string).lower()
    #         element_text = element_text.replace(" ", "")
            
    #         if element_text in invalid_texts or not element.string:
    #             undescriptive_element_status = True
    #         else:
    #             undescriptive_element_status = False  
    #         if element.contents:
    #             for content in element.contents:
    #                 soup2 = BeautifulSoup(str(content), 'html.parser')
    #                 if soup2.find('img') or soup2.find('i'):
    #                     undescriptive_element_status = False
    #         print(undescriptive_element_status)            
            
    #         attr = {}
    #         attr['Page'] = webpage
    #         attr['Element'] = str(element)
    #         attr['Undescriptive_status'] = undescriptive_element_status
    #         all_elements.append(attr)
    #     for f in all_elements:
    #         print(json.dumps(f, indent=2))

a = UndescritiveElementController()
a.undescriptive_element_finder('http://localhost/class8_1/sample.html')
