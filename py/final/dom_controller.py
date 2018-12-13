import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DOMController:

    def get_DOM_time(self, driver, page_link):
        driver.get(page_link)
        #time.sleep(1)
        try:
            navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
            responseStart = driver.execute_script("return window.performance.timing.responseStart")
            domComplete = driver.execute_script("return window.performance.timing.domComplete")

            backendPerformance = responseStart - navigationStart
            frontendPerformance = domComplete - responseStart
        except:
            print("dhora khaichi")    
        return frontendPerformance

    def create_json(self, driver, page_link):
        dom_list=[]
        attr = {}
        attr['Page'] = format(page_link)
        attr['DOM_Load_Time'] = self.get_DOM_time(driver, page_link)    
        dom_list.append(attr)
        return dom_list

    def create_result(self, json_input):
        x = json.loads(json.dumps(json_input))
        return x

# flashScrollController = FlashScrollController()
# driver = flashScrollController.initiate_chrome_driver()
# print(flashScrollController.get_page_height(driver, "http://data.gov.bd/"))
