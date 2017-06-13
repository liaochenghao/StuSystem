# coding: utf-8
from django.db import models


class User(models.Model):
    password = models.CharField(max_length=128, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField('用户名', max_length=50, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)
    ROLE = (
        ('STUDENT', '学生'),
        ('ADMIN', '管理员'),
        ('MARKET', '市场部')
    )
    role = models.CharField(choices=ROLE, max_length=30)

    class Meta:
        db_table = 'user'


class UserInfo(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField('学生姓名', max_length=30)
    email = models.CharField('email', max_length=30)
    wechat = models.CharField('微信号', max_length=30, null=True)
    school = models.CharField('意向学校', max_length=30)
    wcampus = models.CharField('意向校区', max_length=30)
    create_time = models.DateTimeField('新建时间', auto_now=True)
    webid = models.CharField('微信网页登陆返回id', max_length=60, null=True)
    unionid = models.CharField('微信服务号用户unionid', max_length=60, null=True, blank=True)
    openid = models.CharField('微信openid', max_length=60, null=True, unique=True)
    headimgurl = models.CharField('微信头像url', max_length=60, null=True)
    wx_name = models.CharField('微信昵称', max_length=30, null=True)

    class Meta:
        db_table = 'student_info'


class Ticket(models.Model):
    ticket = models.CharField('用户ticket', max_length=100, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    expired_time = models.DateTimeField('过期时间')
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'ticket'