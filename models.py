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
    password = db.Column(db.String(60) , nullable= False)
    posts = db.relationship('Post', backref='author',lazy=True)
    order = db.relationship('Order', backref='owner',lazy=True)

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
    order = db.relationship('Order', backref='product',lazy=True)
    def __repr__(self):
        return f"Post '{self.title}','{self.date_posted}'"

class Order (db.Model):
    id = db.Column(db.Integer , primary_key=True)
    material = db.Column(db.String(20) ,nullable=False)
    size = db.Column(db.String(20) ,nullable=False)
    name = db.Column(db.String(70) ,nullable=False)
    address = db.Column(db.String(150) ,nullable=False)
    phone = db.Column(db.String(70) ,nullable=False)
    color = db.Column(db.String(20) ,nullable=False)
    qty = db.Column(db.Integer ,nullable=False)
    date_ordered =db.Column(db.DateTime ,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'))
    def __repr__(self):
        return f"Post '{self.title}','{self.date_posted}'"

adlo = User.query.filter_by(id=1).first()
class LogModelView(ModelView):

    def is_accessible(self):
        return current_user == adlo

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class LogAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user == adlo

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

path = op.join(op.dirname(__file__), 'static')
admin = Admin(app,index_view=LogAdminIndexView(), template_mode='bootstrap3')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

""" from flask import Flask
from flask import send_file
@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/Examples.pdf"
    return send_file(path, as_attachment=True)
 """ 

admin.add_view(LogModelView(User, db.session))
admin.add_view(LogModelView(Post, db.session))
admin.add_view(LogModelView(Order, db.session))
