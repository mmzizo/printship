from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField ,BooleanField ,TextAreaField ,SelectField ,IntegerField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
from App.models import User

class RegisterationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(),Length(min=2,max=20)])
    phone = StringField('Phone Number' , validators=[DataRequired(),Length(min=11,max=11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators =[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators =[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self , username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken , Please choose different one')
    def validate_email(self , email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken , Please choose different one')
    def validate_phone(self , phone):
        user= User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is already taken , Please choose different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators =[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(),Length(min=2,max=20)])
    phone = StringField('Phone Number' , validators=[DataRequired(),Length(min=11,max=11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Picture', validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('Update')

    def validate_username(self , username):
        if username.data != current_user.username:
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken , Please choose different one')
    def validate_email(self , email):
        if email.data != current_user.email:
            user= User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken , Please choose different one')
    def validate_phone(self , phone):
        if phone.data != current_user.phone:
            user= User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('That phone number is already taken , Please choose different one')

class PostForm(FlaskForm):
    title = StringField('Title' , validators=[DataRequired(),Length(min=2,max=20)])
    caption = TextAreaField('Caption', validators=[DataRequired() ,Length(min=5,max=240)])
    picture = FileField('Thumbnail', validators=[DataRequired() ,FileAllowed(['png','jpg','jpeg'])])
    dfile = FileField('Design file', validators=[DataRequired() ,FileAllowed(['psd','ai','svg','eps','pdf','jpeg','tiff'])])
    submit = SubmitField('Post')

class OrderForm(FlaskForm):
    name = StringField('Name' , validators=[DataRequired(),Length(min=2,max=40)])
    location = TextAreaField('Address', validators=[DataRequired() ,Length(min=5,max=240)])
    phone = StringField('Phone Number' , validators=[DataRequired(),Length(min=11,max=11)])
    material = SelectField(u'Material', choices=['Mug 50 LE','T-shirt 200LE','hoodi 300LE'])
    size = SelectField(u'Size', choices=['S','M','L','XL','XXL','XXXL'])
    color = SelectField(u'color', choices=['black','white','blue','green','red'])
    qty = IntegerField('QTY', validators=[DataRequired()] )
    submit = SubmitField('Order')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')