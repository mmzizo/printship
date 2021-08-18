from datetime import datetime
from App import db , login_manager ,app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin ,login_user ,current_user , login_required , logout_user
from flask_admin.contrib.sqla import ModelView
from flask import url_for,redirect,request 
from flask_admin import Admin ,AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User (db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20) ,unique=True , nullable=False,index=True)
    email = db.Column(db.String(120) ,unique=True , nullable=False)
    phone = db.Column(db.String(120) ,unique=True , nullable=False)
    image_file = db.Column(db.String(20) , nullable=False, default='default.jpg')
    bio = db.Column(db.String(250) ,nullable=False,default='new account')
    password = db.Column(db.String(60) , nullable= False)
    balance = db.Column(db.Integer ,nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True)
    cash = db.relationship('Cashout', backref='applicant',lazy=True)
    order = db.relationship('Order', backref='owner',lazy=True)
    feedback = db.relationship('Feedback', backref='critic',lazy=True)

    def get_reset_token(self, expires_sec=900):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User '{self.username}','{self.email}','{self.image_file}'"

class Post (db.Model):
    __searchable__=['title','caption']
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(20) ,nullable=False,index=True)
    caption = db.Column(db.String(250) ,nullable=False,index=True)
    date_posted =db.Column(db.DateTime ,nullable=False,default=datetime.utcnow)
    image_file = db.Column(db.String(20) , nullable=False, default='defdesign.jpg')
    dfile = db.Column(db.String(20) , nullable=False, default='defdesign.jpg')
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'),nullable=False)
    scorecount = db.Column(db.Integer ,nullable=False,default = 0)
    scoresum = db.Column(db.Integer ,nullable=False,default = 0)
    order = db.relationship('Order', backref='product',lazy=True)
    gallery = db.relationship('Gallery', backref='product',lazy=True)
    feedback = db.relationship('Feedback', backref='rate',lazy=True)
    def __repr__(self):
        return f"Post '{self.title}','{self.date_posted}'"

class Order (db.Model):
    id = db.Column(db.Integer , primary_key=True)
    material = db.Column(db.String(20) ,nullable=False)
    size = db.Column(db.String(20) ,nullable=False)
    name = db.Column(db.String(70) ,nullable=False)
    address = db.Column(db.String(150) ,nullable=False)
    phone = db.Column(db.String(70) ,nullable=False)
    phone2 = db.Column(db.String(70) ,nullable=False)
    color = db.Column(db.String(20) ,nullable=False)
    qty = db.Column(db.Integer ,nullable=False)
    cash = db.Column(db.Integer ,nullable=False)
    status = db.Column(db.String(20) ,nullable=False)
    date_ordered =db.Column(db.DateTime ,nullable=False,default=datetime.utcnow)
    date_shipped =db.Column(db.DateTime ,nullable=True)
    date_recieved =db.Column(db.DateTime ,nullable=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Post '{self.title}','{self.date_posted}'"

class Gallery(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    ig = db.Column(db.String(20) , nullable=False, default='g1.jpg')
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'))

class Cashout(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    requested_cash = db.Column(db.Integer ,nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    

class Feedback(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    cont = db.Column(db.String(250) ,nullable=False,index=True)
    score = db.Column(db.Integer ,nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'))


""" from flask import Flask
from flask import send_file
@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/Examples.pdf"
    return send_file(path, as_attachment=True)
 """ 

