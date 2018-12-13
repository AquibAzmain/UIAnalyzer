from werkzeug.wrappers import Request, Response
from flask import Flask
from flask import render_template, send_from_directory
from flask import request
#import controller.cloner as cloner
import final.site_manager as site_manager
app = Flask(__name__)

@app.route("/")
@app.route('/index')
@app.route('/index.html')
def index():
    rendered = render_template('index.html')
    return rendered

@app.route('/analysis')
@app.route('/analysis.html')
def analysis():
    rendered = render_template('analysis.html')
    return rendered

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
    all_links=[]
    site_url = request.form['search_key']
    if site_url.endswith("/"):
        site_url = site_url[:-1]
    #cloner.crawl(site_url + "/", site_url)
    SiteManager = site_manager.SiteManager()
    if not SiteManager.verify_site(site_url):
        return render_template('error.html')
    else:
        SiteManager = site_manager.SiteManager()
        all_links = SiteManager.get_links(site_url)      
        return render_template('analysis.html', key=site_url, pages=all_links) 

if __name__ == '__main__':
    # from werkzeug.serving import run_simple
    # run_simple(host='0.0.0.0', 9000, app)
    app.run(host='0.0.0.0', debug = True)