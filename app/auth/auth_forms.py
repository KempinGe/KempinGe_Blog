# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,regexp,EqualTo
from wtforms import ValidationError
from ..models import User



class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])

    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')



class RegistrationForm(Form):
    emai = StringField('Email',validators=[Required(), Length(1,64),Email()])
    username = StringField('Username',validators=[Required(),Length(1,64),regexp('[A-Za-z][A-Za-z0-9_.]*$',0,'Username must is Correct format')])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must math')])
    password2 = PasswordField('Confim Password',validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self,field):

        if User.query.filter_by(eamil=field.data).first():
            raise ValidationError('Email already registed')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already  in use')