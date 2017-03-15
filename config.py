#!/usr/bin/evn python
# -*- coding: utf-8 -*-
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送信息
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '656558837@qq.com'
    MAIL_PASSWORD = 'ymjlflcjczkybeia'
    FLASKY_MAIL_SUBJECT_PREFIX = '[XianYun]'
    FLASKY_MAIL_SENDER = 'XianYun Admin <656558837@qq.com>'
    FLASK_ADMIN = '1105234003@qq.com'

    @staticmethod
    def init_app(app):
        pass
class  DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:moji_dev@localhost/xianyun_test'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:moji_dev@localhost/xianyun_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:moji_dev@localhost/xianyun_test'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}