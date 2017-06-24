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