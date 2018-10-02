from bs4 import BeautifulSoup
import requests

r = requests.get('https://api.github.com/events')
print(r.url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())