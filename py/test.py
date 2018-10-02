from werkzeug.wrappers import Request, Response
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    rendered = render_template('home.html')
    return rendered


@app.route("/result", methods=['POST'])
def result():

    searched_word = request.form['search_key']
    rendered = render_template('result.html', key=searched_word)
    return searched_word

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)