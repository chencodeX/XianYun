#!/usr/bin/evn python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template,session,url_for,redirect,current_app,abort,flash,request
from flask_login import login_user,logout_user,login_required,current_user
from . import main
from .forms import EditProfileForm,EditProfileAdminForm,PostForm
from .. import db
from ..model import User,Role,Permission,Post
from ..email import send_email
from ..decorators import admin_required
import os,hashlib,cv2
import numpy as np
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

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        return  redirect(url_for('.index'))
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination,Permission=Permission)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)

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

# @main.route('/edit-avatar',methods=['GET','POST'])
# @login_required
# def edit_avatar():
#     form = ChangeAvatarForm()
#     print '1'
#     if form.validate_on_submit():
#         print '2'
#         AVATAR_BASE_PATH = current_app.config['AVATAR_PATH']
#         print '3'
#         current_user.avatar_base = hashlib.md5((current_user.email+current_user.avatar_base).encode('utf-8')).hexdigest()
#         print '4'
#         base_path_1 = os.path.join(AVATAR_BASE_PATH, current_user.avatar_base + '.png')
#         print '5'
#         form.uploadfile.data.save(base_path_1)
#         print '6'
#         db.session.add(current_user)
#         print '7'
#         return redirect(url_for('.user',username = current_user.username))
#
#     return render_template('edit_avatar.html',form = form)

@main.route('/edit-avatar',methods=['GET','POST'])
@login_required
def edit_avatar():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            AVATAR_BASE_PATH = current_app.config['AVATAR_PATH']
            current_user.avatar_base = hashlib.md5(
                (current_user.email + current_user.avatar_base).encode('utf-8')).hexdigest()
            base_path_1 = os.path.join(AVATAR_BASE_PATH, current_user.avatar_base + '.png')
            file.save(base_path_1)
            image = cv2.imread(base_path_1)
            img_arr = np.array(image)
            [h,w,s]=img_arr.shape
            avg = min(h, w)
            hm = (h - avg)/2
            wm = (w -avg)/2
            out = img_arr[hm:hm + avg, wm:wm + avg, :]
            cv2.imwrite(base_path_1, out)
            db.session.add(current_user)
            return redirect(url_for('.user', username=current_user.username))
        else:
            flash(u'文件格式异常！')
            return render_template('edit_avatar_post.html')
    return render_template('edit_avatar_post.html')

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])

@main.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form  = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash(u'博文已修改！')
    form.body.data = post.body
    return render_template('edit_post.html',form=form)