from __future__ import unicode_literals
from html5parser import HTML5Parser
import requests
from bs4 import BeautifulSoup
import json
import csv

website = "http://localhost/class8_1/sample.html"

r = requests.get(website)
soup = BeautifulSoup(r.text, "html.parser")
tags = []
class EchoParser(HTML5Parser):
    def _printpos(self):
        print ('    Pos: %s' % str(self.getpos()))
        (line, column) = self.getpos()
        print(("line: %d, offset: %d") % (line, column))
        return line

    def _printtag(self, tagtype, tag):
        if tag=="a":
            print ('%s: "%s"' % (tagtype, tag))
            self._printpos()
            return self._printpos()

    def _printattrs(self, attrs):
        if attrs:
            print ('    Attrs:')
            for k, v in attrs:
                print ('       %s = "%s"' % (k, v))
                if k=="href":
                    return v       

    def handle_starttag(self, tag, attrs):
        if tag=="a":
            self._printtag('StartTag', tag)
            self._printattrs(attrs)
            tags.append(self._printtag('StartTag', tag))
            tags.append(self._printattrs(attrs))
            return (self._printtag('StartTag', tag), self._printattrs(attrs))

    def handle_endtag(self, tag):
        if tag=="a":
            self._printtag('EndTag', tag)
            tags.append(self._printtag('EndTag', tag))
            return self._printtag('EndTag', tag)

    def handle_startendtag(self, tag, attrs):
        if tag=="a":
            self._printtag('StartEndTag', tag)
            self._printattrs(attrs)

    def make_json(self, tag, attrs):
        if tag=="a":
            print (self.handle_starttag(tag, attrs))

    # def handle_data(self, data):
    #     print ('Data:')
    #     self._printpos()
    #     for line in data.split('\n'):
    #         print ('    "%s"' % line)

    # def handle_comment(self, data):
    #     print ('Comment: "%s"' % data)
    #     self._printpos()

    # def handle_decl(self, decl):
    #     print ('DocType: "%s"' % decl)
    #     self._printpos()

    # def unknown_decl(self, data):
    #     print ('Unknown: "%s"' % data)
    #     self._printpos()

parser = EchoParser()

# parser.feed('<!DOCTYPE html>\n')
# parser.feed('<h1 id="section1"\nclass="bar">Section 1</h1>\n')
# parser.feed('<p class="foo">foo bar\nbaz blah </p>\n')
# parser.feed('<!-- cool beans! -->\n')
# parser.feed('<hr/>\n')
# parser.feed('<br>\n')
# parser.feed('<p><em>The <strong>End!</strong></em></p>\n')
# parser.feed('<p><em>error</p></em>')
# parser.feed('weird < q <abc@example.com>\n')
parser.feed(r.text)
site_name = "http://localhost/class8_1/"

tags = [tags[i:i + 3] for i in range(0, len(tags), 3)]
print(tags)
tag_json=[]
for tag in tags:
    response_code=200
    link = str(tag[1])
    if "http://" not in link and "https://" not in link and not link.startswith('#'):  
        link = site_name + link

    if tag[1]:
        try:
            r = requests.get(link, verify=False)
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            response_code = 500
                
    attr = {}
    attr['Start_Tag_Location']=tag[0]
    attr['End_Tag_Location']=tag[2]
    attr['href']=tag[1]
    if not tag[1] or tag[1] is None:
        attr['Status'] = 'No link'
        attr['Suggestion'] = 'Add href to this anchor tag'
    elif response_code!=200:
        attr['Status'] = 'Broken link'
        attr['Suggestion'] = 'Provide a valid link'  
    else:
        attr['Status'] = 'Ok'
        attr['Suggestion']= 'None'
    tag_json.append(attr)

anchor_list=[]
attr = {}
attr['Page'] = format(site_name)
attr['Anchor_Tags'] = tag_json

anchor_list.append(attr)

for f in anchor_list:
    print(json.dumps(f, indent=2))    
parser.close()

#csv

x = json.loads(json.dumps(anchor_list))

f = csv.writer(open("anchor_tags.csv", "w", newline=''))

f.writerow(["Page", "Start_Tag_Location", "End_Tag_Location", "Link", "Status", "Suggestion"])
for x in x:
    for anchor_tag in x['Anchor_Tags']:
        #print(anchor_tag.get('Start_Tag_Location'))
        f.writerow([x["Page"],
                    anchor_tag['Start_Tag_Location'],
                    anchor_tag['End_Tag_Location'],
                    anchor_tag['href'],
                    anchor_tag['Status'],
                    anchor_tag['Suggestion'],
                    ])
