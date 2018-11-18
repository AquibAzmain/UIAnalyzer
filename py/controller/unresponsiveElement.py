import requests
from bs4 import BeautifulSoup
import json

website = "http://localhost/shworolipi/"

r = requests.get(website)

def detectUnresElement(req):
    soup = BeautifulSoup(req.text, "html.parser")
    fields = soup.findAll('a')
    a_list = []

    for field in fields:
        attr = {}
        
        attr['name'] = str(field)
        attr['href'] = field.get('href')

        if field.get('href') is None:
            attr['smell_status'] = 'yes'
        else:
            attr['smell_status'] = 'no'

        j = {'a_tags':attr}
        a_list.append(j)

    # for f in a_list:
    #     print(json.dumps(f, indent=2))

    return a_list    


# detectUnresElement(r)