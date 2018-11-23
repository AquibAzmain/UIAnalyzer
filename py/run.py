from werkzeug.wrappers import Request, Response
from flask import Flask
from flask import render_template, send_from_directory
from flask import request
import controller.cloner as cloner
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

@app.route('/<path:path>')
def sendFiles(path):
    return send_from_directory('client/', path)

@app.route("/result", methods=['POST'])
def result():

    site_url = request.form['search_key']
    render_template('result.html', key=site_url)
    cloner.crawl(site_url + "/", site_url)
    return site_url 

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)