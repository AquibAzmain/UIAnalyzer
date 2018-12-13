import requests
import json
import final.crawler_manager as crawler_manager
import final.flash_scroll_controller as flash_scroll_controller
import final.dom_controller as dom_controller
import uuid
class SiteManager:

    def verify_site(self, site):
        if "http://" not in site and "https://" not in site and not site.startswith('#'):
            site = "http://"+site
        try:
            r = requests.get(site, verify=False)
        except requests.exceptions.ConnectionError:
            return False   
        if r.status_code != 200:
            return False
        else:
             return True    

    def get_links(self, site):
        CrawlerManager = crawler_manager.CrawlerManager()
        CrawlerManager.reset()
        CrawlerManager.crawl(site , site)
        return CrawlerManager.visited_links

    def flashScroll(self, driver, all_links, id):
        merged_height_list = []
        flashScrollController = flash_scroll_controller.FlashScrollController()
        for link in all_links:
            height_list = flashScrollController.create_json(driver, link)
            merged_height_list+=height_list
        flashScrollController.create_csv(merged_height_list, id)
        return int(self.average_count(merged_height_list, "Page_Height"))

    def DOMLoadTime(self, driver, all_links):
        merged_dom_list = []
        domController = dom_controller.DOMController()
        for link in all_links:
            dom_list = domController.create_json(driver, link)
            merged_dom_list+=dom_list
        domController.create_result(merged_dom_list)
        print (merged_dom_list)
        return int(self.average_count(merged_dom_list, "DOM_Load_Time"))

    def average_count(self, json_data, attribute):
        return (sum(json_data[attribute] for json_data in json_data))/len(json_data)

    def set_temp_id(self):
        return str(uuid.uuid4())

    def take_screenshot(self, id, site, driver):
        driver.get(site)    
        driver.save_screenshot('client/'+id+'.png')

# SiteManager = SiteManager()
# SiteManager.take_screenshot(2, 'http://www.data.gov.bd/')            