# all the imports
from __future__ import with_statement
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

DEBUG = True
app = Flask(__name__, static_url_path='/static')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/')
def show_result():
    return render_template("main.html")

if __name__ == '__main__':
    app.run()
