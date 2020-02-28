from flask import Flask, request, render_template,session,logging
from flask_bootstrap import Bootstrap
from db.models import User, Msg, Products, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://greg:codevengers@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)


Bootstrap(app)


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

@app.route('/admin/product', methods=['GET', 'POST'])
def contact():
    if request.method=="POST":
        details=request.form
        Product=details['product']
        Price=details['price']
        dscr=details['description']
        file=details['file']
        prod = Products(name=Product, price=Price, description=dscr, photo=file)

        db.session.add(prod)
        db.session.commit()

        return render_template('success.html')
    return render_template('ins-prod.html')

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
#  TODO:
'''  
        1. Security on login (prevents spamming)
        2. Admin Page
        3. buy now page
'''


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
