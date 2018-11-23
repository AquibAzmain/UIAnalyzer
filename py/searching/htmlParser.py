from bs4 import BeautifulSoup
import json
import requests

r = requests.get('http://localhost/class8_1/sample.html', verify=False)
#print(r.url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')
for button in soup.find_all('button'):
    print(button)

  
# print(soup.prettify())
# for link in soup.find_all('a'):
#     invalid_texts = ["clickhere","click","go","click!","link"]
#     undescriptive_link_status = False
#     link_text=""
#     #print("Link href:"+ str(link.get('href')))
    
#     #print ("Link Contents:"+ str(link.contents))
#     link_text = str(link.string).lower()
#     link_text = link_text.replace(" ", "")
#     #print ("Link Text:"+ link_text)
#     if link_text in invalid_texts or not link.string:
#         undescriptive_link_status = True

#     if link.contents:
#         for content in link.contents:
#             soup2 = BeautifulSoup(str(content), 'html.parser')
#             if soup2.find('img') or soup2.find('i'):
#                 #print('pailam')
#                 undescriptive_link_status = False

#     #print (undescriptive_link_status)


def undescriptive_link_finder(link_tag):
    soup = BeautifulSoup(link_tag, 'html.parser')
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
        return undescriptive_link_status


#undescriptive_link_finder('<p>Sample3 <a href="sample2.html">Click here</a></p>')        
