import json
import csv
import requests
from bs4 import BeautifulSoup
class UndescriptiveElementController:
    def undescriptive_finder(self, webpage):
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
            if undescriptive_element_status:
                attr['Suggestion'] = "Provide meaningful text for this element"
            else:
                attr['Suggestion'] = "None"    
            all_elements.append(attr)
        return all_elements

    def create_csv(self, json_input, id):
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/undescriptive_element_'+id+'.csv', "w", newline=''))
        f.writerow(["Page", "Element", "Undescriptive Status", "Suggestion"])
        for x in x:
            page_name = (x["Page"]).encode('ascii', 'ignore')
            element_name = (x["Element"]).encode('ascii', 'ignore')
            f.writerow([page_name,element_name,x["Undescriptive_status"],x["Suggestion"]])
        return x

    def get_found_parcent(self, json_input):
        smell_count = 0
        result = {}
        for x in json_input:
            if x['Undescriptive_status']:
                smell_count = smell_count + 1
        result['Total_Count'] = len(json_input)
        result['Smell_Count'] = smell_count
        result['Smell_Parcent'] = int(smell_count*100/len(json_input))
        return result     
    
