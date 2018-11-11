import urllib3

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

http = urllib3.PoolManager()
response = http.request('GET', url)
webContent = response.read()

print(webContent[0:300])