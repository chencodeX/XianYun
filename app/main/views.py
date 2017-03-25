#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template,session,url_for,redirect,current_app,abort,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm
from .. import db
from ..model import User,Role
from ..email import send_email
from ..decorators import admin_required

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username = form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data,role_id=3)
#             db.session.add(user)
#             session['know']=False
#             if current_app.config['FLASK_ADMIN']:
#                 send_email(current_app.config['FLASK_ADMIN'],'新用户注册',
#                            'mail/new_user',user=user)
#         else:
#             session['know']=True
#         session['name'] = form.name.data
#         # old_name = session.get('name')
#         # print 'dd'
#         # if old_name is not None and old_name !=form.name.data:
#         #     print 'dd1'
#         #     flash(u'用户变更')
#         # session['name'] = form.name.data
#         # form.name.data = ''
#         return redirect(url_for('main.index'))
#     return render_template('index.html', form=form, name=session.get('name'),
#                            known=session.get('know',False))

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的信息已更新！')
        return redirect(url_for('.user',username = current_user.username))
    form.name.data = current_user.name
    form.location.data =current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form = form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'用户信息已更新！')
        return redirect(url_for('.user',username = user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form = form,user=user)