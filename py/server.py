from werkzeug.wrappers import Request, Response
from flask import Flask
from flask import render_template, send_from_directory
from flask import request

app = Flask(__name__)

@app.route("/")
@app.route('/index')
@app.route('/index.html')
def index():
    rendered = render_template('index.html')
    return rendered

@app.route('/<path:path>')
def sendFiles(path):
    return send_from_directory('.', path)

@app.route("/result", methods=['POST'])
def result():

    searched_word = request.form['search_key']
    rendered = render_template('result.html', key=searched_word)
    return searched_word

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)