# coding: utf-8
from django.db import models
from authentication.models import User
from course.models import Project


class Order(models.Model):
    CURRENCY = (
        ('DOLLAR', '美金'),
        ('RMB', '人民币')
    )
    PAYMENT = (
        ('ON_LINE', '线上支付'),
        ('TRANSFER_ACCOUNT', '转账'),
        ('OFF_LINE', '面付')
    )
    STATUS = (
        ('TO_PAY', '待支付'),
        ('PAYED', '已支付')
    )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    currency = models.CharField('币种', choices=CURRENCY, max_length=30)
    payment = models.CharField('支付方式', choices=PAYMENT, max_length=30)
    status = models.CharField('订单状态', choices=STATUS, max_length=30, default='TO_PAY')
    standard_fee = models.FloatField('标准费用')
    pay_fee = models.FloatField('支付费用')
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'