# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    name = models.CharField('姓名', max_length=30, null=True)
    password = models.CharField(max_length=128, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField('用户名', max_length=50, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)
    is_superuser = models.BooleanField('是否为超级用户', default=False)
    ROLE = (
        ('STUDENT', '学生'),
        ('ADMIN', '管理员'),
        ('MARKET', '市场部'),
        ('FINANCE', '财务部')
    )
    role = models.CharField(choices=ROLE, max_length=30)
    USERNAME_FIELD = 'username'
    qr_code = models.CharField('二维码', max_length=255, null=True)

    class Meta:
        db_table = 'user'


class UserInfo(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField('学生姓名', max_length=30)
    email = models.EmailField('email', max_length=30)
    wechat = models.CharField('微信号', max_length=30)
    cschool = models.CharField('当前学校', max_length=30)
    wschool = models.CharField('意向学校', max_length=60)
    wcampus = models.CharField('意向校区', max_length=60)
    create_time = models.DateTimeField('新建时间', auto_now=True)
    webid = models.CharField('微信网页登陆返回id', max_length=60, null=True)
    unionid = models.CharField('微信服务号用户unionid', max_length=60, null=True, blank=True, unique=True)
    openid = models.CharField('微信openid', max_length=60, null=True, unique=True)
    headimgurl = models.CharField('微信头像url', max_length=255, null=True)
    wx_name = models.CharField('微信昵称', max_length=30, null=True)

    first_name = models.CharField('First Name', max_length=30, null=True)
    last_name = models.CharField('Last name', max_length=30, null=True)
    phone = models.CharField('联系手机', max_length=11)
    GENDER = (
        ('MALE', '男'),
        ('FEMALE', '女')
    )
    gender = models.CharField('性别', choices=GENDER, max_length=30)
    id_number = models.CharField('身份证号/护照号', max_length=30, unique=True, null=True)
    major = models.CharField('专业', max_length=30, null=True)
    graduate_year = models.CharField('毕业年份', max_length=30, null=True)
    gpa = models.FloatField('GPA')

    class Meta:
        db_table = 'student_info'


class UserInfoRemark(models.Model):
    user_info = models.ForeignKey(UserInfo, related_name='user_info_remark')
    remark = models.CharField('备注', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_info_remark'


class Ticket(models.Model):
    user = models.ForeignKey(User)
    ticket = models.CharField('用户ticket', max_length=100, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    expired_time = models.DateTimeField('过期时间')

    class Meta:
        db_table = 'ticket'


class UserScoreDetail(models.Model):
    user = models.ForeignKey(User)
    department = models.CharField('收件部门', max_length=30)
    phone = models.CharField('联系电话', max_length=30)
    country = models.CharField('收件国家', max_length=30)
    post_code = models.CharField('邮编', max_length=30)
    address = models.CharField('详细地址', max_length=60)

    class Meta:
        db_table = 'student_score_detail'