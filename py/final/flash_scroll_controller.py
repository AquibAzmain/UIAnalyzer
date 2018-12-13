import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class FlashScrollController:

    def get_page_height(self, driver, page_link):
        page_height = 0
        driver.get(page_link)
        #time.sleep(1)
        try:
            page_height= driver.execute_script("return document.body.scrollHeight;")
        except:
            print("dhora khaichi")    
        return page_height

    def create_json(self, driver, page_link):
        height_list=[]
        attr = {}
        attr['Page'] = format(page_link)
        attr['Page_Height'] = self.get_page_height(driver, page_link)
        if attr['Page_Height']<=1556:
            attr['Status'] = 'Ok'
            attr['Suggestion'] = 'None'
        else:
            attr['Status'] = 'Flash Scrolling'
            attr['Suggestion'] = 'Page height =< 1556 px'    
        height_list.append(attr)
        return height_list

    def create_csv(self, json_input, id):
        x = json.loads(json.dumps(json_input))
        f = csv.writer(open('client/flash_scrolling_'+id+'.csv', "w", newline=''))
        f.writerow(["Page", "Height(px)", "Status", "Suggestion"])
        for x in x:
            page_name = (x["Page"]).encode('ascii', 'ignore')
            f.writerow([page_name,x["Page_Height"],x["Status"],x["Suggestion"]])
        return x

# flashScrollController = FlashScrollController()
# driver = flashScrollController.initiate_chrome_driver()
# print(flashScrollController.get_page_height(driver, "http://data.gov.bd/"))
