#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm

from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import Required,Length,Email,Regexp,EqualTo

from ..model import User
class LoginForm(FlaskForm):
    email = StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
    password = PasswordField(u'密码',validators=[Required()])
    remember_me = BooleanField(u'保持在线')
    submit = SubmitField(u'登陆')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'Usernames must have only letters, '
                                          u'numbers, dots or underscores')])
    password = PasswordField(u'密码',validators=[Required(),EqualTo('password2',message=u'密码需要保持一致')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self,field):
        # print 'email_error'
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已存在')

    def validate_username(self,field):
        # print 'name_error'
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')