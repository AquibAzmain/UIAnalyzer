import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumManager:
    def initiate_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("window-size=1366,768")
        # chrome_options.add_argument("--start-maximized") # doesnt work for headless, go with window-size
        chrome_options.add_argument("--headless")  
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
        return driver

