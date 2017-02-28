# -*- coding:utf-8 -*-
from datetime import datetime
from flask import render_template,session,redirect,url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/')
def index():
    return render_template('index.html')
# @main.route('/',methods = ['GET','POST'])
# def home():
#     form = NameForm()
#     if form.validate_on_submit:
#         session['isFirstRequest'] = True
#         old_name = session.get('name')
#         print('jiuzhishi%s' %old_name)
#         print(form.name.data)
#         user = User.query.filter_by(username = form.name.data).first()
#         if user is None:
#             user = User(username = form.name.data)
#             db.session.add(user)
#             session['known'] = False
#             print('cirenshixinrentianjiadaoshujuku')
#         else:
#             # if old_name is not None and old_name != form.name.data:
#             #    flash('name change',category='warning')
#             session['known'] = True
#             print('huanyinghuilai')
#
#
#
#         session['name'] = form.name.data
#         form.name.data = ''
#
#         return redirect(url_for('.home'))
#     print(session.get('known'))
#     render_template('index/html',form=form ,name=session.get('name'),known=session.get('known'),current_time=datetime.utcnow())