from bs4 import BeautifulSoup
import json
import requests

r = requests.get('https://bangladesh.gov.bd/index.php', verify=False)
print(r.url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())
for link in soup.find_all('a'):
    print(link.get('href'))

soup.find_all('a')
