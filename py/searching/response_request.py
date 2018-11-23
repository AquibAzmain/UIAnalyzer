import requests
import time

response = requests.get('https://stackoverflow.com/questions/5909/get-size-of-a-file-before-downloading-in-python')
print (len(response.content))


with requests.get('https://stackoverflow.com/questions/5909/get-size-of-a-file-before-downloading-in-python', stream=True) as response:
    size = sum(len(chunk) for chunk in response.iter_content(8196))
print(size)


r = requests.head('https://stackoverflow.com/questions/5909/get-size-of-a-file-before-downloading-in-python')
print(r.headers)