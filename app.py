from flask import Flask, request, render_template,session,logging
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://greg:root@localhost/VM'

db=SQLAlchemy(app)
# Tabelul MySQL de login

class User(db.Model):
    __tablename__="Login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Msg(db.Model):
    __tablename__="Messages"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    message=db.Column(db.String(255))

class Products(db.Model):
    __tablename__="Products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    photo= db.Column(db.String(50))
        

@app.route('/products/<who>')
def shop(who):
    product=Products.query.filter_by(name=who).first()
    if product is None:
        return render_template('404.html'), 404
    else:
        return render_template('product.html', product=product)
@app.route('/')
def index():
    prod = Products.query.all()
    
    return render_template("index.html",prod=prod)
@app.route('/info')
def info():
    return render_template("info.html")

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


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        
        login = User.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return render_template("success.html")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']

        register = User(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return render_template("success.html")
    return render_template("register.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=="POST":
        details=request.form
        Name=details['name']
        Email=details['email']
        Message=details['msg']
        contact = Msg(name=Name, email=Email, message=Message)

        db.session.add(contact)
        db.session.commit()

        return render_template('success.html')
    return render_template('contact.html')

@app.route('/pareri')
def received():
    data = Msg.query.all()
    
    return render_template('out.html' ,data = data)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
