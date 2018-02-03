# coding: utf-8
from django.db import models


class PaymentAccountInfo(models.Model):
    """支付账号"""
    PAYMENT = (
        ('ALI_PAY', '支付宝转账'),
        # ('WECHAT', '微信转账'),
        ('PAY_PAL', 'PayPal'),
        ('BANK', '银行转账')
    )
    CURRENCY = (
        ('FOREIGN_CURRENCY', '外币'),
        ('RMB', '人民币')
    )
    currency = models.CharField('币种', choices=CURRENCY, default='RMB', max_length=30)
    bank_name = models.CharField('银行名称(pay_pal)', max_length=60, null=True)
    account_number = models.CharField('账号', max_length=30)
    account_name = models.CharField('账户姓名(beneficiary company name)', max_length=60)
    opening_bank = models.CharField('开户行地址(bank address)', max_length=60, null=True)
    payment = models.CharField(choices=PAYMENT, max_length=30, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    company_address = models.CharField('公司地址(pay_pal)', max_length=60, null=True)
    routing_number_paper = models.CharField('routing number paper & electronic(pay_pal)', max_length=30, null=True)
    routing_number_wires = models.CharField('routing number wires(pay_pal)', max_length=30, null=True)
    swift_code = models.CharField('swift code us dollar', max_length=30, null=True)
    swift_code_foreign_currency = models.CharField('swift code foreign currency', max_length=30, null=True)
    pay_link = models.CharField('快捷支付短链接(外币银行转账)', max_length=30, null=True)

    class Meta:
        db_table = 'payment_account_info'
        unique_together = ['payment', 'currency']