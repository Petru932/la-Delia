from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

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
    price = db.Column(db.Float)
    description = db.Column(db.String(255))
    photo= db.Column(db.String(50))