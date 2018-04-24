# coding: utf-8
from source.models import Project, Course
from django.db import models

from authentication.models import User, StudentScoreDetail


class ShoppingChart(models.Model):
    """购物车"""
    STATUS = (
        ('NEW', '新添加'),
        ('ORDERED', '已下单'),
        ('PAYED', '已支付'),
        ('DELETED', '已删除')
    )
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course_num = models.IntegerField('课程数量')
    course_fee = models.FloatField('课程费用')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('状态', max_length=30, choices=STATUS, default='NEW')

    class Meta:
        db_table = 'shopping_chart'


class Order(models.Model):
    """订单"""
    CURRENCY = (
        ('FOREIGN_CURRENCY', '外币'),
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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_number = models.CharField('订单号', max_length=30, null=True, unique=True)
    currency = models.CharField('币种', choices=CURRENCY, max_length=30, null=True)
    payment = models.CharField('支付方式', choices=PAYMENT, max_length=30, null=True)
    status = models.CharField('订单状态', choices=STATUS, max_length=30, default='TO_PAY')
    standard_fee = models.FloatField('标准费用')
    pay_fee = models.FloatField('支付费用', null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    remark = models.CharField('订单备注', max_length=255, null=True)
    coupon_list = models.CharField('优惠券列表', null=True, max_length=255)

    class Meta:
        db_table = 'order'


class OrderChartRelation(models.Model):
    """订单与商品关系"""
    chart = models.ForeignKey(ShoppingChart, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_chart_relation'


class UserCourse(models.Model):
    """用户选课表"""
    STATUS = (
        ('TO_UPLOAD', '未审课'),
        ('TO_CONFIRM', '审课中'),
        ('PASS', '审课通过'),
        ('NOPASS', '审课失败')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    score = models.IntegerField('课程成绩分数', null=True)
    score_grade = models.CharField('课程等级', max_length=30, null=True)
    reporting_time = models.DateTimeField('成绩录入时间', null=True)
    confirm_img = models.ImageField('审课照片', upload_to='course/confirm_img', null=True)
    confirm_remark = models.CharField('审课备注', max_length=255, blank=True, null=True)
    status = models.CharField('学生审课状态', choices=STATUS, default='TO_UPLOAD', max_length=30)
    post_datetime = models.DateTimeField('快递时间', null=True)
    post_channel = models.CharField('快递方式', max_length=30, null=True)
    post_number = models.CharField('快递单号', max_length=30, null=True)
    CREDIT_SWITCH_STATUS = (
        ('PRE_POSTED', '成绩待寄出'),
        ('POSTED', '成绩已寄出'),
        ('SWITCHED', '学分已转换')
    )
    credit_switch_status = models.CharField(max_length=30, choices=CREDIT_SWITCH_STATUS, default='PRE_POSTED')
    switch_img = models.ImageField('学分转换结果证明', upload_to='project/result/photo/', null=True)
    switch_remark = models.CharField('学分转换备注', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_course'


class OrderPayment(models.Model):
    """订单支付信息"""
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    amount = models.FloatField('支付金额', null=True)
    account_number = models.CharField('支付账号', max_length=60, null=True)
    account_name = models.CharField('支付姓名', max_length=60, null=True)
    opening_bank = models.CharField('开户银行', max_length=60, null=True)
    pay_date = models.DateField('支付日期', auto_now_add=True, null=True)
    img = models.ImageField(upload_to='order/order_payment')
    remark = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_payment'
