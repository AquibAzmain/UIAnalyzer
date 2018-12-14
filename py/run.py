from werkzeug.wrappers import Request, Response
from flask import Flask
from flask import render_template, send_from_directory
from flask import request
#import controller.cloner as cloner
import final.site_manager as site_manager
import final.selenium_manager as selenium_manager
app = Flask(__name__)


@app.route("/")
@app.route('/index')
@app.route('/index.html')
def index():
    rendered = render_template('index.html')
    return rendered


# @app.route('/analysis')
# @app.route('/analysis.html')
# def analysis():
#     rendered = render_template('analysis.html')
#     return rendered


@app.route('/error')
@app.route('/error.html')
def error():
    rendered = render_template('error.html')
    return rendered


@app.route('/<path:path>')
def sendFiles(path):
    return send_from_directory('client/', path)


@app.route("/result", methods=['POST'])
def result():
    all_links = []
    site_url = request.form['search_key']
    if site_url.endswith("/"):
        site_url = site_url[:-1]
    SiteManager = site_manager.SiteManager()
    if not SiteManager.verify_site(site_url):
        return render_template('error.html')
    else:
        SiteManager = site_manager.SiteManager()
        temp_id = SiteManager.set_temp_id()

        SeleniumManager = selenium_manager.SeleniumManager()
        driver = SeleniumManager.initiate_chrome_driver()

        all_links = SiteManager.get_links(site_url)

        dom_height_object = {}
        dom_height_object = SiteManager.DOMScroll(driver, all_links, temp_id)
        average_height = dom_height_object["Page_Height"]
        average_dom_load_time = dom_height_object["DOM_Load_Time"]
        flash_scroll_parcent = dom_height_object["Smell_Parcent"]
        slow_page_parcent = dom_height_object["Slow_Page_Parcent"]
        page_object = dom_height_object["Page_Object"]

        anchor_tag_object = {}
        anchor_tag_object = SiteManager.anchor(all_links, temp_id)
        broken_link_parcent = anchor_tag_object["Smell_Parcent"]

        undescriptive_element_object = {}
        undescriptive_element_object = SiteManager.undescriptive(
            all_links, temp_id)
        undescriptive_element_parcent = undescriptive_element_object["Smell_Parcent"]

        unformatted_element_object = {}
        unformatted_element_object = SiteManager.unformatted(all_links, temp_id)
        unformatted_element_parcent = unformatted_element_object["Smell_Parcent"]

        SiteManager.take_screenshot(temp_id, site_url, driver)
        total_count = anchor_tag_object["Total_Count"] + \
            undescriptive_element_object["Total_Count"] + \
            dom_height_object["Total_Count"] + unformatted_element_object["Total_Count"]
        smell_count = anchor_tag_object["Smell_Count"] + \
            undescriptive_element_object["Smell_Count"] + \
            dom_height_object["Smell_Count"] + unformatted_element_object["Smell_Count"]
        smell_parcent = int(smell_count*100/total_count)
        ok_parcent = 100-smell_parcent
        smell_per_page = int(smell_count/len(all_links))
        return render_template(
            'analysis.html',
            key=site_url,
            pages=page_object,
            id=temp_id,
            average_height=average_height,
            average_dom_load_time=average_dom_load_time,
            flash_scroll_parcent=flash_scroll_parcent,
            slow_page_parcent=slow_page_parcent,
            broken_link_parcent=broken_link_parcent,
            undescriptive_element_parcent=undescriptive_element_parcent,
            unformatted_element_parcent=unformatted_element_parcent,
            total_count=total_count,
            smell_count=smell_count,
            ok_parcent=ok_parcent,
            smell_parcent=smell_parcent,
            smell_per_page=smell_per_page)


if __name__ == '__main__':
    # from werkzeug.serving import run_simple
    # run_simple(host='0.0.0.0', 9000, app)
    app.run(host='0.0.0.0', port=9000, debug=True)
