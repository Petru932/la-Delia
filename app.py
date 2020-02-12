from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
@app.route('/info')
def developer():
    return render_template("Dev.html")
@app.route('/user/<name>')
def user(name):
    return render_template("user.html",name=name)
@app.route('/client')
def client():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

if __name__ == '__main__':
    app.run()
