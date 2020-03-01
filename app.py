from flask import Flask, request, render_template,session,logging
from flask_bootstrap import Bootstrap
from db.models import User, Msg, Products, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY']= 'a secret key'




admin=input("Numele admin-ului MySQL: ")
psk=input("Parola ta MySQL: ")
pos = input("Este Server-ul tau local ? (Da/Nu): ")
if pos.lower() ==  "nu" or pos.lower()== "no":
    pos=input("IP-ul Server-ului tau: ")
    key_p = 'mysql://'+ admin+':'+psk+'@'+pos+'/Shop'
else:
    key_p = 'mysql://'+admin+':'+psk+'@localhost/Shop'

app.config['SQLALCHEMY_DATABASE_URI']=key_p

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)




@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)


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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route('/login',methods=["GET", "POST"])
def login():
    if request.method=="POST":
        uname = request.form["username"]
        passw = request.form["password"]
        usr = User.query.filter_by(username=uname, password=passw).first()
        login_user(usr)
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']

        register = User(username = uname, email = mail,password=generate_password_hash(passw) )
        db.session.add(register)
        db.session.commit()

        return render_template("success.html")
    return render_template("register.html")
@app.route('/not-finished')
def trick():
    return render_template("devs.html")
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("success.html")

with app.app_context():
    db.create_all()

admin = Admin(app, name='Admin la Delia', template_mode='bootstrap3')


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Msg, db.session))
admin.add_view(ModelView(Products, db.session))


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
