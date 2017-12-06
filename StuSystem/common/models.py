# coding: utf-8
from django.db import models

from authentication.models import User


class SalesMan(models.Model):
    """
    销售人员model
    """
    name = models.CharField('姓名', max_length=30)
    wechat = models.CharField('微信号', max_length=30)
    email = models.EmailField('邮箱', max_length=30)
    qr_code = models.ImageField('二维码', upload_to='common/sales_man/')

    class Meta:
        db_table = 'sales_man'

    def __str__(self):
        return self.name


class SalesManUser(models.Model):
    """
    销售人员与User关系表
    """
    STATUS = (
        ('NEW', '新关注'),
        ('CONTACTED', '已联系'),
    )
    user = models.ForeignKey(User)
    sales_man = models.ForeignKey(SalesMan)
    status = models.CharField('用户状态', max_length=30, choices=STATUS, default='NEW')
    create_time = models.DateTimeField(auto_now=True)
    remark = models.CharField('备注', max_length=255, null=True)

    class Meta:
        db_table = 'sales_man_user'


class FirstLevel(models.Model):
    """导航栏一级目录"""
    name = models.CharField('一级目录名称', max_length=20)
    key = models.CharField('一级目录key', max_length=30)
    rank = models.IntegerField('排序', null=True)

    class Meta:
        db_table = 'first_level'
        unique_together = ['key']


class FirstLevelRole(models.Model):
    """一级目录与角色间关系"""
    pre = models.ForeignKey(FirstLevel)
    role = models.CharField('角色名称', choices=User.ROLE, max_length=30)

    class Meta:
        db_table = 'first_level_role'


class SecondLevel(models.Model):
    """导航栏二级目录"""
    name = models.CharField('二级目录名称', max_length=20)
    key = models.CharField('二级目录key', max_length=30)
    rank = models.IntegerField('排序', null=True)
    icon = models.CharField('图标类型', max_length=30)

    class Meta:
        db_table = 'second_level'


class FirstSecondRelation(models.Model):
    """一二级目录关系"""
    first = models.ForeignKey(FirstLevel)
    second = models.ForeignKey(SecondLevel)

    class Meta:
        db_table = 'first_second_relation'


class SecondLevelRole(models.Model):
    """二级目录与角色间关系"""
    pre = models.ForeignKey(SecondLevel)
    role = models.CharField('角色名称', choices=User.ROLE, max_length=30)

    class Meta:
        db_table = 'second_level_role'