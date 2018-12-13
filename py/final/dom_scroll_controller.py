import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DOMScrollController:

    def get_page_height_DOM(self, driver, page_link):
        data_object = {}
        page_height = 0
        frontendPerformance = 0
        driver.get(page_link)
        #time.sleep(1)
        try:
            page_height= driver.execute_script("return document.body.scrollHeight;")
            responseStart = driver.execute_script("return window.performance.timing.responseStart")
            domComplete = driver.execute_script("return window.performance.timing.domComplete")
            frontendPerformance = domComplete - responseStart
            data_object['Page_Height'] = page_height
            data_object['DOM_Load_Time'] = frontendPerformance
        except:
            print("dhora khaichi")

        return data_object

    def create_json(self, driver, page_link):
        data_object = {}
        data_object = self.get_page_height_DOM(driver, page_link)
        height_dom_list=[]
        attr = {}
        attr['Page'] = format(page_link)
        attr['Page_Height'] = data_object['Page_Height']
        attr['DOM_Load_Time'] = data_object['DOM_Load_Time']
        if attr['Page_Height']<=1556:
            attr['Status'] = 'Ok'
            attr['Suggestion'] = 'None'
        else:
            attr['Status'] = 'Flash Scrolling'
            attr['Suggestion'] = 'Page height =< 1556 px'    
        height_dom_list.append(attr)
        return height_dom_list

    def create_csv(self, json_input, id):
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/flash_scrolling_'+id+'.csv', "w", newline=''))
        f.writerow(["Page", "Height(px)", "Status", "Suggestion"])
        for x in x:
            page_name = (x["Page"]).encode('ascii', 'ignore')
            f.writerow([page_name,x["Page_Height"],x["Status"],x["Suggestion"]])
        return x

    def get_found_parcent(self, json_input):
        fresh_count = 0
        smell_count = 0
        for x in json_input:
            if x['Status']=='Ok':
                fresh_count = fresh_count + 1
        smell_count = len(json_input) - fresh_count
        return int(smell_count*100/len(json_input))        
# flashScrollController = FlashScrollController()
# driver = flashScrollController.initiate_chrome_driver()
# print(flashScrollController.get_page_height(driver, "http://data.gov.bd/"))
