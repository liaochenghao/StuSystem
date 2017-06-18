# coding: utf-8
from django.db import models


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