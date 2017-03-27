#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField,FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import Required,Length,Email,Regexp
from  wtforms import ValidationError
from ..model import Role,User

class NameForm(FlaskForm):
    name = StringField(u'你的名字?', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0,64)])
    location = StringField(u'地址', validators=[Length(0,64)])
    about_me = TextAreaField(u'个人介绍')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'Usernames must have only letters, '
                                          u'numbers, dots or underscores')])
    confirmed = BooleanField(u'已验证')
    role = SelectField(u'用户角色', coerce=int)

    name = StringField(u'真实姓名', validators=[Length(0,64)])
    location = StringField(u'地址', validators=[Length(0,64)])
    about_me = TextAreaField(u'个人介绍')
    submit = SubmitField(u'提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已存在')

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')

class ChangeAvatarForm(FlaskForm):
    uploadfile=FileField(u'上传头像',validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(u'提交')
