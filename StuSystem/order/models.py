# coding: utf-8
from coupon.models import Coupon
from course.models import Project, Course
from django.db import models

from authentication.models import User


class Order(models.Model):
    CURRENCY = (
        ('DOLLAR', '美金'),
        ('RMB', '人民币')
    )
    PAYMENT = (
        ('BANK', '银行转账'),
        ('ALI_PAY', '支付宝转账'),
        ('PAY_PAL', 'PAY_PAL支付'),
        ('OFF_LINE', '面付')
    )
    STATUS = (
        ('CANCELED', '已取消'),
        ('TO_PAY', '待支付'),
        ('TO_CONFIRM', '待确认'),
        ('CONFIRMED', '已确认'),
        ('CONFIRM_FAILED', '验证失败')
    )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    currency = models.CharField('币种', choices=CURRENCY, max_length=30)
    payment = models.CharField('支付方式', choices=PAYMENT, max_length=30)
    status = models.CharField('订单状态', choices=STATUS, max_length=30, default='TO_PAY')
    standard_fee = models.FloatField('标准费用')
    pay_fee = models.FloatField('支付费用')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    course_num = models.IntegerField()
    remark = models.CharField('订单备注', max_length=255, null=True)
    coupon_list = models.CharField('优惠券列表', null=True, max_length=255)

    class Meta:
        db_table = 'order'


class UserCourse(models.Model):
    """用户选课表"""
    STATUS = (
        ('TO_UPLOAD', '待上传'),
        ('TO_CONFIRM', '待审核'),
        ('PASS', '通过'),
        ('NOPASS', '不通过')
    )
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    order = models.ForeignKey(Order)
    create_time = models.DateTimeField(auto_now=True)
    score = models.IntegerField('课程成绩分数', default=0)
    score_grade = models.CharField('课程等级', max_length=30, null=True)
    reporting_time = models.DateTimeField('成绩录入时间', null=True)
    confirm_photo = models.ImageField('审课照片', upload_to='course/confirm_photo', null=True)
    status = models.CharField('学生审课状态', choices=STATUS, default='TO_UPLOAD', max_length=30)

    class Meta:
        db_table = 'user_course'


class OrderPayment(models.Model):
    """订单支付信息"""
    order = models.ForeignKey(Order)
    amount = models.FloatField()
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