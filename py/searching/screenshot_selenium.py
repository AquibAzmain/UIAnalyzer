import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("window-size=1366,768")
# chrome_options.add_argument("--start-maximized") # doesnt work for headless, go with window-size
chrome_options.add_argument("--headless")  


driver = webdriver.Chrome(executable_path='./../chromedriver.exe', chrome_options=chrome_options)

driver.get('http://www.data.gov.bd/')    
time.sleep(5)

driver.save_screenshot('shot2.png')

html = driver.page_source
html = driver.execute_script("return document.body.innerHTML")
