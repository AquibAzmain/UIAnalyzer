import json
import csv

json1 = "[{'Page': 'http://localhost/class8_1/index.php', 'Anchor_Tags': [{'Start_Tag_Location': 55, 'End_Tag_Location': 55, 'href': 'registration.php', 'Status': 'Ok', 'Suggestion': 'None'}, {'Start_Tag_Location': 59, 'End_Tag_Location': 59, 'href': 'index.php', 'Status': 'Ok', 'Suggestion': 'None'}, {'Start_Tag_Location': 55, 'End_Tag_Location': 55, 'href': 'registration.php', 'Status': 'Ok', 'Suggestion': 'None'}]}]"
json2 = "[{'Page': 'http://localhost/class8_1/registration.php', 'Anchor_Tags': [{'Start_Tag_Location': 55, 'End_Tag_Location': 55, 'href': 'registration.php','Status': 'Ok', 'Suggestion': 'None'}, {'Start_Tag_Location': 59, 'End_Tag_Location': 59, 'href': 'index.php', 'Status': 'Ok', 'Suggestion': 'None'}]}]"

#merged_dict = {key: value for (key, value) in (json1 + json2)}
#jsonString_merged = json.dumps(merged_dict)

#print(json1[1:len(json1)-1] + json2[1:len(json2)-1])

merged_json = json1[1:len(json1)-1] + ',' + json2[1:len(json2)-1]
for f in json1[1:len(json1)-1]:
    print(json.dumps(f, indent=2))  


def create_csv(json_input):
        #x = json.loads(json.dumps(json_input))
        x = json_input
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
create_csv(merged_json)