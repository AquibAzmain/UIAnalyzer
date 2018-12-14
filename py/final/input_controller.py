import requests
from bs4 import BeautifulSoup
import json
import csv


class InputController:
    def unformatted_input_finder(self, website):
        skip = ["select", "submit", "reset", "button", "file", "email", "password", "radio", "checkbox",
                "color", "date", "datetime-local", "month", "number", "range", "tel", "time", "url", "week", "hidden"]
        try:
            r = requests.get(website, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
            pass
        soup = BeautifulSoup(r.text, "html.parser")
        fields = soup.findAll('input')
        field_list = []

        for field in fields:
            attr = {}
            if field.get('type') in skip or field.get('size') or field.get('maxlength') or field.get('min') or field.get('max') or field.get('pattern'):
                attr['Page'] = website
                attr['Element'] = str(field)
                attr['Status'] = 'Ok'
                attr['Suggestion'] = 'None'
            else:
                attr['Page'] = website
                attr['Element'] = str(field)
                attr['Status'] = 'Unformatted input'
                attr['Suggestion'] = 'Add maxlength or pattern attribute or use a specified input type'
            field_list.append(attr)
        return field_list

    def create_csv(self, json_input, id):
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/unformatted_input_' +
                            id+'.csv', "w", newline=''))
        f.writerow(["Page", "Element", "Unformatted Status", "Suggestion"])
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

# test = InputController()
# test.unformatted_input_finder("http://localhost/class8_1/sample.html")
