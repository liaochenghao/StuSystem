# coding: utf-8
from django.db import models
from authentication.models import User
from course.models import Project
from coupon.models import Coupon


class Order(models.Model):
    CURRENCY = (
        ('DOLLAR', '美金'),
        ('RMB', '人民币')
    )
    PAYMENT = (
        # ('ON_LINE', '线上支付'),
        ('BANK', '银行转账'),
        ('ALI_PAY', '支付宝转账'),
        ('OFF_LINE', '面付')
    )
    STATUS = (
        ('CANCELED', '已取消'),
        ('TO_PAY', '待支付'),
        ('PAYED', '已支付'),
        ('CONFIRMED', '已确认')
    )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    currency = models.CharField('币种', choices=CURRENCY, max_length=30)
    payment = models.CharField('支付方式', choices=PAYMENT, max_length=30)
    status = models.CharField('订单状态', choices=STATUS, max_length=30, default='TO_PAY')
    standard_fee = models.FloatField('标准费用')
    pay_fee = models.FloatField('支付费用', null=True)
    create_time = models.DateTimeField(auto_now=True)
    course_num = models.IntegerField()
    remark = models.CharField('订单备注', max_length=255, null=True)

    class Meta:
        db_table = 'order'


class OrderPayment(models.Model):
    order = models.ForeignKey(Order)
    account_number = models.CharField('支付账号', max_length=30)
    account_name = models.CharField('支付姓名', max_length=30)
    opening_bank = models.CharField('开户银行', max_length=30, null=True)
    pay_date = models.DateField('支付日期')
    img = models.ImageField(upload_to='order/order_payment')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_payment'


class OrderCoupon(models.Model):
    order = models.ForeignKey(Order)
    coupon = models.ForeignKey(Coupon)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_coupon'