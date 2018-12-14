import requests
import json
import final.crawler_manager as crawler_manager
import final.dom_scroll_controller as dom_scroll_controller
import final.a_controller as a_controller
import final.undescriptive_element_controller as undescriptive_element_controller
import final.input_controller as input_controller
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

    def DOMScroll(self, driver, all_links, id):
        merged_list = []
        data_object = {}
        DOMScrollController = dom_scroll_controller.DOMScrollController()
        for link in all_links:
            scroll_dom_list = DOMScrollController.create_json(driver, link)
            merged_list+=scroll_dom_list
        if merged_list:    
            DOMScrollController.create_csv(merged_list, id)
            data_object['Smell_Parcent'] = DOMScrollController.get_found_parcent(merged_list, 'Status')["Smell_Parcent"]
            data_object['Smell_Count'] = DOMScrollController.get_found_parcent(merged_list, 'Status')["Smell_Count"]
            data_object['Total_Count'] = DOMScrollController.get_found_parcent(merged_list, 'Status')["Total_Count"]
            data_object['Page_Height'] = self.average_count(merged_list, "Page_Height")
            data_object['DOM_Load_Time'] = self.average_count(merged_list, "DOM_Load_Time")
            data_object['Slow_Page_Count'] = DOMScrollController.get_found_parcent(merged_list, 'DOM_Load')["Smell_Count"]
            data_object['Slow_Page_Parcent'] = DOMScrollController.get_found_parcent(merged_list, 'DOM_Load')["Smell_Parcent"]
            data_object['Page_Object'] = merged_list
        return data_object   

    def anchor(self, all_links, id):
        merged_list = []
        anchor_list = []
        data_object = {}
        AnchorTagController = a_controller.AController()
        for link in all_links:
            anchor_list = AnchorTagController.broken_link_finder(link)
            merged_list+=anchor_list
        if merged_list:       
            AnchorTagController.create_csv(merged_list, id)
            data_object = AnchorTagController.get_found_parcent(merged_list)
        else:
            data_object = {'Total_Count': 0,'Smell_Count': 0,'Smell_Parcent': 0}    
        return data_object     

    def undescriptive(self, all_links, id):
        merged_list = []
        element_list = []
        data_object = {}
        UndescriptiveElementController = undescriptive_element_controller.UndescriptiveElementController()
        for link in all_links:
            element_list = UndescriptiveElementController.undescriptive_finder(link)
            merged_list+=element_list
        if merged_list:       
            UndescriptiveElementController.create_csv(merged_list, id)
            data_object = UndescriptiveElementController.get_found_parcent(merged_list)
        else:
            data_object = {'Total_Count': 0,'Smell_Count': 0,'Smell_Parcent': 0}    
        return data_object

    def unformatted(self, all_links, id):
        merged_list = []
        element_list = []
        data_object = {}
        InputController = input_controller.InputController()
        for link in all_links:
            element_list = InputController.unformatted_input_finder(link)
            merged_list+=element_list
        if merged_list:       
            InputController.create_csv(merged_list, id)
            data_object = InputController.get_found_parcent(merged_list)
        else:
            data_object = {'Total_Count': 0,'Smell_Count': 0,'Smell_Parcent': 0}    
        return data_object    

    def average_count(self, json_data, attribute):
        return int((sum(json_data[attribute] for json_data in json_data))/len(json_data))

    def set_temp_id(self):
        return str(uuid.uuid4())

    def take_screenshot(self, id, site, driver):
        driver.get(site)    
        driver.save_screenshot('client/'+id+'.png')

# SiteManager = SiteManager()
# SiteManager.take_screenshot(2, 'http://www.data.gov.bd/')            