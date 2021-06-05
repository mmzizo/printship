from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] ='93cff4d54ae58dcc14cf3ba7f8f14e11'

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =False
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'
db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] =True
app.config['MAIL_USERNAME'] = 'printshipllc'
app.config['MAIL_PASSWORD'] = 'uswzrdrtxdhesnni'
mail =Mail(app)

from App import routes