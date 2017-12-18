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
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    course_num = models.IntegerField('课程数量')
    course_fee = models.FloatField('课程费用')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('状态', max_length=30, choices=STATUS, default='NEW')
    stu_score_detail = models.ForeignKey(StudentScoreDetail, verbose_name='学生成绩地址', null=True)

    class Meta:
        db_table = 'shopping_chart'


class Order(models.Model):
    """订单"""
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
    currency = models.CharField('币种', choices=CURRENCY, max_length=30)
    payment = models.CharField('支付方式', choices=PAYMENT, max_length=30)
    status = models.CharField('订单状态', choices=STATUS, max_length=30, default='TO_PAY')
    standard_fee = models.FloatField('标准费用')
    pay_fee = models.FloatField('支付费用')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    remark = models.CharField('订单备注', max_length=255, null=True)
    coupon_list = models.CharField('优惠券列表', null=True, max_length=255)

    class Meta:
        db_table = 'order'


class OrderChartRelation(models.Model):
    """订单与商品关系"""
    chart = models.ForeignKey(ShoppingChart)
    order = models.ForeignKey(Order)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_chart_relation'


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
    project = models.ForeignKey(Project)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    score = models.IntegerField('课程成绩分数')
    score_grade = models.CharField('课程等级', max_length=30, null=True)
    reporting_time = models.DateTimeField('成绩录入时间', null=True)
    confirm_img = models.ImageField('审课照片', upload_to='course/confirm_img', null=True)
    status = models.CharField('学生审课状态', choices=STATUS, default='TO_UPLOAD', max_length=30)
    post_datetime = models.DateTimeField('快递时间', null=True)
    post_channel = models.CharField('快递方式', max_length=30, null=True)
    post_number = models.CharField('快递单号', max_length=30, null=True)
    CREDIT_SWITCH_STATUS = (
        ('PRE_POSTED', '成绩待寄出'),
        ('POSTED', '成绩单已寄出'),
        ('RECEIVED', '学校已收到'),
        ('SUCCESS', '学分转换成功'),
        ('FAILURE', '学分转换失败')
    )
    credit_switch_status = models.CharField(max_length=30, choices=STATUS, default='PRE_POSTED')
    switch_img = models.ImageField('学分转换结果证明', upload_to='project/result/photo/', null=True)

    class Meta:
        db_table = 'user_course'


class OrderPayment(models.Model):
    """订单支付信息"""
    order = models.ForeignKey(Order)
    amount = models.FloatField('支付金额')
    account_number = models.CharField('支付账号', max_length=30)
    account_name = models.CharField('支付姓名', max_length=30)
    opening_bank = models.CharField('开户银行', max_length=30, null=True)
    pay_date = models.DateField('支付日期')
    img = models.ImageField(upload_to='order/order_payment')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_payment'