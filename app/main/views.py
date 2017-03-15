#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template,session,url_for,redirect,current_app

from . import main
from .forms import NameForm
from .. import db
from ..model import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username=form.name.data,role_id=3)
            db.session.add(user)
            session['know']=False
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'],'新用户注册',
                           'mail/new_user',user=user)
        else:
            session['know']=True
        session['name'] = form.name.data
        # old_name = session.get('name')
        # print 'dd'
        # if old_name is not None and old_name !=form.name.data:
        #     print 'dd1'
        #     flash(u'用户变更')
        # session['name'] = form.name.data
        # form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('know',False))
