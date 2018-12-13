import json
import csv
import requests
from final.anchorparser_controller import AnchorparserController
requests.packages.urllib3.disable_warnings()
class AnchorTagController:
    def create_json(self,website):
        r = requests.get(website, verify=False)
        tags = []
        parser = AnchorparserController()
        parser.reset()
        parser.feed(r.text)
        tags = parser.tags

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

    def create_csv(self, json_input, id):
        x = []
        x = json.loads(json.dumps(json_input))
        print (len(x))
        f = csv.writer(open('client/anchor_tags_'+id+'.csv', "w", newline=''))

        f.writerow(["Page", "Start_Tag_Location", "End_Tag_Location", "Link", "Status", "Suggestion"])
        for x in x:
            for anchor_tag in x['Anchor_Tags']:
                if anchor_tag['href']:
                    href = anchor_tag['href'].encode('ascii', 'ignore')
                else:
                    href = anchor_tag['href']    
                #print(anchor_tag.get('Start_Tag_Location'))
                f.writerow([x["Page"].encode('ascii', 'ignore'),
                            anchor_tag['Start_Tag_Location'],
                            anchor_tag['End_Tag_Location'],
                            href,
                            anchor_tag['Status'],
                            anchor_tag['Suggestion'],
                            ])
 
    def get_found_parcent(self, json_input):
        fresh_count = 0
        smell_count = 0
        total_count = 0
        result = {}
        for x in json_input:
            for anchor_tag in x['Anchor_Tags']:
                total_count = total_count + 1
                if anchor_tag['Status']=='Ok':
                    fresh_count = fresh_count + 1
        smell_count = total_count - fresh_count
        result['Total_Count'] = total_count
        result['Smell_Count'] = smell_count
        result['Smell_Parcent'] = int(smell_count*100/total_count)
        return result