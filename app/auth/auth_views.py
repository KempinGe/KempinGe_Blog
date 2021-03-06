# -*- coding:utf-8 -*-
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user

from app import db
from . import auth
from ..models import User
from .auth_forms import LoginForm,RegistrationForm
from flask_login import logout_user, login_required,current_user
from ..emails import send_email


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid username or password')


    return render_template('auth/login.html',form = form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    return redirect(url_for('main.index'))


@auth.route('/register',methods = ['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.emai.data,username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm you account','auth/email/confirm',user=user,token=token)

        flash('A eamil has been sent to you by email')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('you have confirm your account thanks')
    else:
        flash('the confirm link is invalid or has been expired')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static' :
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'confirm you account','auth/email/confirm',user=current_user,token=token)
    flash('a new email has been send to your email')
    return redirect(url_for('main.index'))

