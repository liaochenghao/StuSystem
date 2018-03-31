# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    ROLE = (
        ('STUDENT', '学生'),
        ('ADMIN', '管理员'),
        ('MARKET', '市场部'),
        ('PRODUCT', '产品部'),
        ('FINANCE', '财务部'),
        ('SALES', '销售部')
    )
    name = models.CharField('姓名', max_length=100, null=True)
    password = models.CharField(max_length=128, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField('用户名', max_length=50, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)
    is_superuser = models.BooleanField('是否为超级用户', default=False)
    unionid = models.CharField('微信unionid', max_length=255, null=True)
    openid = models.CharField('微信openid', max_length=255, null=True)
    s_openid = models.CharField('署校联盟小程序openid', max_length=255, null=True)
    role = models.CharField(choices=ROLE, max_length=30)
    USERNAME_FIELD = 'username'
    qr_code = models.CharField('二维码', max_length=255, null=True)
    channel_id = models.IntegerField(verbose_name='用户渠道信息', null=True)
    recommend_user = models.ForeignKey('self', verbose_name='推荐的用户', null=True)
    bind_sales_man = models.CharField('绑定CC', max_length=50, null=True)

    class Meta:
        db_table = 'user'


class UserInfo(models.Model):
    GENDER = (
        ('MALE', '男'),
        ('FEMALE', '女')
    )
    GRADE = (
        ('GRADE_ONE', '大一'),
        ('GRADE_TWO', '大二'),
        ('GRADE_THREE', '大三'),
        ('GRADE_FOUR', '大四'),
        ('GRADE_FIVE', '大五')
    )
    STUDENT_STATUS = (
        ('NEW', '新建用户'),
        ('PERSONAL_FILE', '已建档'),
        ('ADDED_CC', '已添加CC'),
        ('SUPPLY_ORDER', '已提交订单'),
        ('PAYMENT_CONFIRM', '待缴费确认'),
        ('TO_CHOOSE_COURSE', '待选课'),
        ('PICKUP_COURSE', '已选课'),
        ('TO_CONFIRMED', '待审课确认'),
        ('CONFIRMED_COURSE', '已审课'),
        ('AFTER_SCORE', '已出成绩'),
        ('SWITCH_CREDIT', '学分转换中'),
        ('SWITCHED_COURSE', '已学分转换')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField('学生姓名', max_length=30, null=True)
    english_name = models.CharField('英文名称', max_length=30, null=True)
    first_language = models.CharField('母语', max_length=30, null=True)
    ielts_scores = models.CharField('雅思成绩', max_length=30, null=True)
    email = models.EmailField('email', max_length=30, null=True)
    wechat = models.CharField('微信号', max_length=30, null=True)
    cschool = models.CharField('当前学校', max_length=30, null=True)
    wcampus = models.TextField('意向校区', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    webid = models.CharField('微信网页登陆返回id', max_length=60, null=True)
    unionid = models.CharField('微信服务号用户unionid', max_length=60, null=True, unique=True)
    openid = models.CharField('微信openid', max_length=60, null=True, unique=True)
    s_openid = models.CharField('署校联盟小程序openid', max_length=255, null=True, unique=True)
    headimgurl = models.CharField('微信头像url', max_length=255, null=True)
    wx_name = models.CharField('微信昵称', max_length=30, null=True)
    phone = models.CharField('联系手机', max_length=11, null=True)
    gender = models.CharField('性别', choices=GENDER, max_length=30, null=True)
    id_number = models.CharField('身份证号/护照号', max_length=30, unique=True, null=True)
    major = models.CharField('专业', max_length=30, null=True)
    graduate_year = models.CharField('毕业年份', max_length=30, null=True)
    gpa = models.FloatField('GPA', null=True)
    birth_date = models.DateField('出生日期', null=True)
    grade = models.CharField(choices=GRADE, default='GRADE_ONE', max_length=10, null=True)
    sales_man = models.CharField('销售顾问', max_length=60, null=True)
    valid_sales_man = models.BooleanField('是否添加销售顾问微信', default=False)
    student_status = models.CharField(choices=STUDENT_STATUS, default='NEW', max_length=60, null=True)

    class Meta:
        db_table = 'student_info'
        ordering = ['-create_time']

    @property
    def school_info(self):
        return {
            'cschool': self.cschool,
            'major': self.major,
            'graduate_year': self.graduate_year,
            'gpa': self.gpa
        }


class UserInfoRemark(models.Model):
    """用户信息备注"""
    user_info = models.ForeignKey(UserInfo, related_name='user_info_remark', on_delete=models.DO_NOTHING)
    remark_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    remark = models.CharField('备注', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_info_remark'
        ordering = ['-create_time']


class StudentScoreDetail(models.Model):
    """用户成绩邮寄信息"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    country = models.CharField('国家', max_length=60, null=True)
    province_post_code = models.CharField('具体的州/省的邮编', max_length=30, null=True)
    university = models.CharField('大学名称', max_length=30, null=True)
    department = models.CharField('院系名称', max_length=30, default=None, null=True)
    transfer_department = models.CharField('转学分部门/办公楼', max_length=30, null=True)
    transfer_office = models.CharField('具体办公室', max_length=30, null=True)
    address = models.CharField('详细地址', max_length=60, default=None, null=True)
    teacher_name = models.CharField('收件老师姓名', max_length=30, default=None, null=True)
    phone = models.CharField('联系电话', max_length=30, null=True)
    email = models.CharField('邮箱', max_length=30, default=None, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'student_score_detail'
