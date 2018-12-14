import requests
from bs4 import BeautifulSoup
import json
import csv
requests.packages.urllib3.disable_warnings()

class AController:

    def verify_site(self, site):
        try:
            r = requests.get(site, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
            return False 
        if r.status_code != 200:
            return False
        else:
             return True 

    def broken_link_finder(self, website):
        try:
            r = requests.get(website, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
            pass
        soup = BeautifulSoup(r.text, "html.parser")
        fields = soup.findAll('a')
        field_list = []
        for field in fields:
            link = field.get('href')
            try:
                if "http://" not in link and "https://" not in link and not link.startswith('#'):
                    link = website + link
            except TypeError:
                pass        
            attr = {}
            if not field.get('href'):
                attr['Page'] = website
                attr['Element'] = str(field)
                attr['Status'] = 'No link'
                attr['Suggestion'] = 'Add href to this anchor tag'
            # elif not self.verify_site(link):
            #     attr['Page'] = website
            #     attr['Element'] = str(field)
            #     attr['Status'] = 'Broken link'
            #     attr['Suggestion'] = 'Provide a valid link'    
            else:
                attr['Page'] = website
                attr['Element'] = str(field)
                attr['Status'] = 'Ok'
                attr['Suggestion'] = 'None'
            field_list.append(attr)   
        return field_list

    def create_csv(self, json_input, id):
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/anchor_tags_' +
                            id+'.csv', "w", newline=''))
        f.writerow(["Page", "Element", "Status", "Suggestion"])
        for x in x:
            page_name = (x["Page"]).encode('ascii', 'ignore')
            element_name = (x["Element"]).encode('ascii', 'ignore')
            f.writerow([page_name, element_name, x["Status"], x["Suggestion"]])
        return x

    def get_found_parcent(self, json_input):
        fresh_count = 0
        smell_count = 0
        total_count = 0
        result = {}
        for x in json_input:
            total_count = total_count + 1
            if x['Status'] == 'Ok':
                fresh_count = fresh_count + 1
        smell_count = total_count - fresh_count
        result['Total_Count'] = total_count
        result['Smell_Count'] = smell_count
        result['Smell_Parcent'] = int(smell_count*100/total_count)
        return result

# test = AController()
# test.broken_link_finder("https://bangladesh.gov.bd/site/page/13d5cd57-8430-4d83-ac76-ca14de906b32/")
