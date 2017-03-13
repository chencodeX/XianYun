#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from flask import Flask ,render_template,session,url_for,redirect
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

# import sys
# default_encoding = 'utf-8'
# reload(sys)
# sys.setdefaultencoding(default_encoding)

class NameForm(FlaskForm):
    name = StringField(u'你的名字?', validators=[Required()])
    submit = SubmitField(u'提交')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wojiaxiaokezuihaokan,jiushitianshangdexiaoxiannv!'
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/user/<name>')
def User(name):
    # return '<h1>hello, %s</h1>'% name
    return render_template('user.html',name = name)

@app.route('/user/<int:id>')
def User_id(id):
    # return '<h1>hello, %s</h1>'% str(id+2)
    return render_template('base.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    # app.run('127.0.0.1',debug=True)
    manager.run()