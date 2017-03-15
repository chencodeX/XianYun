#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from flask import Flask ,render_template,session,url_for,redirect,flash
from flask import request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail,Message
from threading import Thread
# import sys
# default_encoding = 'utf-8'
# reload(sys)
# sys.setdefaultencoding(default_encoding)

class NameForm(FlaskForm):
    name = StringField(u'你的名字?', validators=[Required()])
    submit = SubmitField(u'提交')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wojiaxiaokezuihaokan,jiushitianshangdexiaoxiannv!'

#数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:moji_dev@localhost/xianyun_test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#邮件发送信息
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '656558837@qq.com'
app.config['MAIL_PASSWORD'] = 'ymjlflcjczkybeia'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[XianYun]'
app.config['FLASKY_MAIL_SENDER'] = 'XianYun Admin <656558837@qq.com>'
app.config['FLASK_ADMIN']='1105234003@qq.com'

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)



def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username=form.name.data,role_id=3)
            db.session.add(user)
            session['know']=False
            if app.config['FLASK_ADMIN']:
                send_email(app.config['FLASK_ADMIN'],'新用户注册',
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
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('know',False))


@app.route('/user/<name>')
def User_1(name):
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
    db.create_all()
    manager.run()
    # db.create_all()
    # admin_role = Role(name='Admin')  # 实例化
    # mod_role = Role(name='Moderator')
    # user_role = Role(name='User')
    # user_john = User(username='zihao.chen', role=admin_role)  # role属性也可使用，虽然他不是真正的数据库列，但却是一对多关系的高级表示
    # user_susan = User(username='test1', role=user_role)
    # user_david = User(username='test2', role=user_role)
    # db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan,
    #                     user_david])  # 准备把对象写入数据库之前，先要将其添加到会话中，数据库会话db.session和Flask session对象没有关系，数据库会话也称事物
    # db.session.commit()  # 提交会话到数据库