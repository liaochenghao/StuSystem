# coding: utf-8
from django.db import models


class PaymentAccountInfo(models.Model):
    """支付账号"""
    PAYMENT = (
        ('ALI_PAY', '支付宝转账'),
        # ('WECHAT', '微信转账'),
        ('PAY_PAL', 'PAY_PAL转账'),
        ('BANK', '银行转账')
    )
    CURRENCY = (
        ('DOLLAR', '美金'),
        ('RMB', '人民币')
    )
    currency = models.CharField('币种', choices=CURRENCY, default='RMB', max_length=30)
    account_number = models.CharField('账号', max_length=30, unique=True)
    account_name = models.CharField('账户姓名', max_length=30)
    opening_bank = models.CharField('开户行', max_length=30, null=True)
    payment = models.CharField(choices=PAYMENT, max_length=30, unique=True)
    swift_code = models.CharField(max_length=30, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_account_info'