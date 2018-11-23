import json
import csv
import requests
from anchorparser_controller import AnchorparserController
class AnchorTagController:
    def create_json(self,website):
        r = requests.get(website)
        tags = []
        parser = AnchorparserController()
        parser.feed(r.text)
        tags = parser.tags

        # site_name = "http://localhost/class8_1/"

        tags = [tags[i:i + 3] for i in range(0, len(tags), 3)]
        tag_json=[]
        for tag in tags:
            response_code=200
            link = str(tag[1])
            if "http://" not in link and "https://" not in link and not link.startswith('#'):  
                link = website + link

                # if tag[1]:
                #     try:
                #         r = requests.get(link, verify=False)
                #     except requests.exceptions.ConnectionError:
                #         response_code = 500
                        
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
        attr['Page'] = format(website)
        attr['Anchor_Tags'] = tag_json

        anchor_list.append(attr)
        parser.close()
        return anchor_list

    def create_csv(self, json_input):
        x = json.loads(json.dumps(json_input))

        f = csv.writer(open("../results/anchor_tags.csv", "w", newline=''))

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


# website = "http://localhost/class8_1/sample.html"
# anchorTagController = AnchorTagController()
# anchor_list = anchorTagController.create_json(website)
# anchorTagController.create_csv(anchor_list)

# for f in anchor_list:
#     print(json.dumps(f, indent=2))   