from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
Bootstrap(app)

#MySQL Config
app.secret_key = 'your secret key'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='greg'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']= 'VM'



@app.route('/')
def index():
    return render_template("index.html")
@app.route('/info')
def info():
    return render_template("Dev.html")
@app.route('/user/<name>')
def user(name):
    return render_template("user.html",name=name)

@app.route('/client')
def client():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/alex')
def alex():
    return render_template('alex.html')

mysql=MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=="POST":
        details=request.form
        Name=details['name']
        Email=details['email']
        Message=details['msg']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO Messages VALUES (%s, %s, %s)", (Name, Email,Message))
        mysql.connection.commit()
        cur.close()
        return render_template('success.html')
    return render_template('contact.html')

@app.route('/data')
def db():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM Messages")
    mysql.connection.commit()
    rows = []

    for row in cur:
        rows.append(row)
        print(row)
    data = cur.fetchall()    
    return render_template('out.html', data = data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
