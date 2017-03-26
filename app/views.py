from flask import Flask, render_template, request, url_for

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/submittochain', methods=['POST'])
def login():
    print(request.form['aadhar'])
    return "hello"

app = Flask(__name__)