#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from flask import render_template,redirect,request,url_for,flash,current_app
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from ..model import User
from .forms import LoginForm,RegistrationForm
from .. import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户邮箱或密码错误')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已经退出登录')
    return  redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    app = current_app._get_current_object()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        send_email(app.config['FLASK_ADMIN'], '新用户注册',
                   'mail/new_user', user=user)
        flash(u'你现在已经可以登录啦~')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form = form)

# @auth.route('/confirm/<token>')
# @login_required
# def con