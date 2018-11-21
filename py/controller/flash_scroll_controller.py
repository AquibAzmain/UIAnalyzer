import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class FlashScrollController:
    def initiate_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("window-size=1366,768")
        # chrome_options.add_argument("--start-maximized") # doesnt work for headless, go with window-size
        chrome_options.add_argument("--headless")  
        driver = webdriver.Chrome(executable_path='./../chromedriver.exe', chrome_options=chrome_options)
        return driver

    def get_page_height(self, driver, page_link):
        page_height = 0
        driver.get(page_link)
        time.sleep(1)
        page_height= driver.execute_script("return document.body.scrollHeight;")
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

    def create_csv(self, json_input):
        x = json.loads(json.dumps(json_input))

        f = csv.writer(open("../results/flash_scrolling.csv", "w", newline=''))

        f.writerow(["Page", "Height(px)", "Status", "Suggestion"])
        for x in x:
            f.writerow([x["Page"],x["Page_Height"],x["Status"],x["Suggestion"]])