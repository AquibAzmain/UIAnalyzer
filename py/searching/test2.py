import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("window-size=1366,768")
# chrome_options.add_argument("--start-maximized") # doesnt work for headless, go with window-size
chrome_options.add_argument("--headless")  


driver = webdriver.Chrome(executable_path='./../chromedriver.exe', chrome_options=chrome_options)

driver.get('https://www.mediacollege.com/internet/javascript/page/scroll.html')
time.sleep(5)


#driver.save_screenshot('shot2.png')

# html = driver.page_source
#html = driver.execute_script("return document.body.innerHTML")


exec_time = driver.execute_script("var t0 = performance.now();window.scrollTo(0, 500);var t1 = performance.now();return (t1-t0);")
print(exec_time)

test_height= driver.execute_script("return document.body.scrollHeight;")
screen_height = driver.execute_script("return screen.availHeight;")
print(test_height)
print(screen_height)

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
end = time.time()
print(lenOfPage)
match=False
while(match==False):
    lastCount = lenOfPage
    #time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True
print(lenOfPage)

start = time.time()
testScroll = driver.execute_script("window.scrollTo(0, 5000000);")
end = time.time()
print(end - start)

driver.quit()