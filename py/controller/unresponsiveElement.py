import requests
from bs4 import BeautifulSoup
import json

website = "http://www.humansofthakurgaon.org/"

r = requests.get(website)
soup = BeautifulSoup(r.text, "html.parser")
html_text = soup.prettify()
html_text = html_text.splitlines()
def detectUnresElement(req):
    soup = BeautifulSoup(req.text, "html.parser")
    html_text = soup.prettify()
    html_text = html_text.splitlines()

    fields = soup.findAll('a')
    a_list = []

    for field in fields:
        attr = {}
        # if any(field.get('href') in s for s in html_text):
        #     print("paichi")

        href_location = extract_location(html_text, field.get('href'))
        attr['location']=href_location 

        # attr['name'] = str(field)
        attr['href'] = field.get('href')

        if field.get('href') is None and r.status_code != 200:
            attr['smell_status'] = 'yes'
        else:
            attr['smell_status'] = 'no'

        j = {'a_tags':attr}
        a_list.append(j)

    for f in a_list:
        print(json.dumps(f, indent=2))
    

    return a_list    

def extract_location(html_text, href_text):
    for idx, val in enumerate(html_text):
        temp_arr = []
        temp = BeautifulSoup(val, "html.parser")
        temp_arr = temp.findAll('a')
        if len(temp_arr)>0 and temp_arr[0].get('href') == href_text:
            return idx

detectUnresElement(r)