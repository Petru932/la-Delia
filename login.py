from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='codevengers'
app.config['MYSQL_DB']= 'shop'

mysql=MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Login WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            '''session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']'''
            return render_template('success.html')
        else: 
            return render_template("404.html")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')