# coding: utf-8
from django.db import models


class PaymentAccountInfo(models.Model):
    PAYMENT = (
        ('ALI_PAY', '支付宝转账'),
        # ('WECHAT', '微信转账'),
        ('BANK', '银行转账')
    )
    account_number = models.CharField('账号', max_length=30, unique=True)
    account_name = models.CharField('账户姓名', max_length=30)
    opening_bank = models.CharField('开户行', max_length=30, null=True)
    payment = models.CharField(choices=PAYMENT, max_length=30, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_account_info'