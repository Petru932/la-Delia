from flask import Flask, render_template, request
from flask_mysqldb import MySQL 
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.config['MYSQL_HOST']='192.168.1.207'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='codevengers'
app.config['MYSQL_DB']= 'shop'

mysql=MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        details=request.form
        firstName=details['fname']
        lastName=details['lname']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return render_template('success.html')
    return render_template('db.html')

@app.route('/out')
def db():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM MyUsers")
    mysql.connection.commit()
    rows = []

    for row in cur:
        rows.append(row)
        print(row)
    data = cur.fetchall()    
    return render_template('out.html', data = data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')