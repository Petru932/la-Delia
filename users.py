from flask import Flask, render_template, request
from flask_mysqldb import MySQL 
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='codevengers'
app.config['MYSQL_DB']= 'shop'

mysql=MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
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

@app.route('/out')
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
    app.run(host='0.0.0.0')