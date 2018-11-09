from bs4 import BeautifulSoup
import json
import requests

r = requests.get('http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168')
print(r.url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())
for link in soup.find_all('a'):
    print(link.get('href'))

soup.find_all('a')    