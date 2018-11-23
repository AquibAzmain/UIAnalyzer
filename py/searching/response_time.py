import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
chrome_options = Options()
chrome_options.add_argument("window-size=1366,768")
# chrome_options.add_argument("--start-maximized") # doesnt work for headless, go with window-size
chrome_options.add_argument("--headless")  


driver = webdriver.Chrome(executable_path='./../chromedriver.exe', chrome_options=chrome_options)


source = "https://stackoverflow.com/questions/21268328/what-exactly-is-page-response-time"
driver.get(source)

navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
responseStart = driver.execute_script("return window.performance.timing.responseStart")
domComplete = driver.execute_script("return window.performance.timing.domComplete")

backendPerformance = responseStart - navigationStart
frontendPerformance = domComplete - responseStart

print ("Back End: %s" % backendPerformance)
print ("Front End: %s" % frontendPerformance)

driver.quit()

time = requests.get('https://stackoverflow.com/questions/21268328/what-exactly-is-page-response-time', verify=False).elapsed.total_seconds() 
print(time) 