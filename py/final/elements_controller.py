import json
import csv
import requests
from final.anchorparser_controller import AnchorparserController
requests.packages.urllib3.disable_warnings()


class AnchorTagController:
    def create_json(self, website):
        tags = []
        tag_json = []
        r = requests.get(website, verify=False)
        parser = AnchorparserController()
        parser._reset()
        parser.feed(r.text)
        tags = parser.tags

        tags = [tags[i:i + 3] for i in range(0, len(tags), 3)]
        for tag in tags:
            response_code = 200
            link = str(tag[1])
            if "http://" not in link and "https://" not in link and not link.startswith('#'):
                link = website + link
            if tag[1]:
                try:
                    r = requests.get(link, verify=False)
                except requests.exceptions.ConnectionError:
                    response_code = 500
            print(response_code)            
            attr = {}
            attr['Page'] = format(website)
            attr['Start_Tag_Location'] = tag[0]
            attr['End_Tag_Location'] = tag[2]
            attr['href'] = tag[1]
            if not tag[1] or tag[1] is None:
                attr['Status'] = 'No link'
                attr['Suggestion'] = 'Add href to this anchor tag'
            elif response_code != 200:
                attr['Status'] = 'Broken link'
                attr['Suggestion'] = 'Provide a valid link'
            else:
                attr['Status'] = 'Ok'
                attr['Suggestion'] = 'None'
            tag_json.append(attr)
        parser.close()
        return tag_json

    def create_csv(self, json_input, id):
        x = []
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/anchor_tags_'+id+'.csv', "w", newline=''))

        f.writerow(["Page", "Start_Tag_Location",
                    "End_Tag_Location", "Link", "Status", "Suggestion"])
        for anchor_tag in x:
            if not anchor_tag['href']:
                href = ""
            else:
                href = anchor_tag['href'].encode('ascii', 'ignore')
                # print(anchor_tag.get('Start_Tag_Location'))
            f.writerow([anchor_tag["Page"].encode('ascii', 'ignore'),
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
            total_count = total_count + 1
            if x['Status'] == 'Ok':
                fresh_count = fresh_count + 1
        smell_count = total_count - fresh_count
        result['Total_Count'] = total_count
        result['Smell_Count'] = smell_count
        result['Smell_Parcent'] = int(smell_count*100/total_count)
        return result
