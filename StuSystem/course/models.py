# coding: utf-8
from django.db import models

from authentication.models import User


class CampusType(models.Model):
    """
    校区类型表
    """
    title = models.CharField('暑校类型', max_length=30, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        db_table = "campus_type"

    def __str__(self):
        return self.title


class CampusCountry(models.Model):
    """
    暑校类型对应国家
    """
    name = models.CharField('国家名称', max_length=30, unique=True)
    campus_type = models.ForeignKey(CampusType)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'campus_country'

    def __str__(self):
        return self.name


class Campus(models.Model):
    """
    校区信息表
    """
    name = models.CharField('校区名称', max_length=30)
    info = models.CharField("校区描述", max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = "campus"

    def __str__(self):
        return self.name


class CampusCountryRelation(models.Model):
    """校区和国家关系表"""
    campus = models.ForeignKey(Campus)
    campus_country = models.ForeignKey(CampusCountry)

    class Meta:
        db_table = 'campus_country_relation'


class Project(models.Model):
    """项目表"""
    campus = models.ForeignKey(Campus)
    name = models.CharField('项目名称', max_length=30, null=True)
    start_date = models.DateField('开始时间')
    end_date = models.DateField('结束时间')
    address = models.CharField('上课地点', max_length=100, null=True)
    info = models.CharField('项目描述', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    apply_fee = models.FloatField('申请费', null=True)
    course_num = models.IntegerField('课程数')
    campus_country = models.ForeignKey(CampusCountry, null=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name

    @property
    def current_applyed_number(self):
        from order.models import Order
        data = set(Order.objects.all().values_list('user_id', flat=True))
        return len(data)

    @property
    def current_payed_number(self):
        from order.models import Order
        data = set(Order.objects.filter(status='CONFIRMED').values_list('user_id', flat=True))
        return len(data)


class ProjectCourseFee(models.Model):
    """项目课程费用对应表"""
    project = models.ForeignKey(Project, related_name='project_course_fee')
    course_number = models.IntegerField('课程门数')
    course_fee = models.FloatField('课程费用')

    class Meta:
        db_table = 'project_course_fee'

    @property
    def get_course_info(self):
        return '%d门' % self.course_number


class Course(models.Model):
    project = models.ForeignKey(Project)
    course_code = models.CharField('课程代码', max_length=30, unique=True)
    name = models.CharField('课程名称', max_length=30)
    max_num = models.IntegerField('最大容纳人数')
    credit = models.IntegerField('学分')
    professor = models.CharField('授课教授', max_length=30)
    start_time = models.CharField('上课开始时间', max_length=30)
    end_time = models.CharField('上课结束时间', max_length=30)
    address = models.CharField('上课地点', max_length=30)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    syllabus = models.CharField('课程大纲', null=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name


class ProjectResult(models.Model):
    """用户学分转换"""
    STATUS = (
        ('POSTED', '成绩单已寄出'),
        ('RECEIVED', '学校已收到'),
        ('SUCCESS', '学分转换成功'),
        ('FAILURE', '学分转换失败')
    )
    user = models.OneToOneField(User)
    create_time = models.DateTimeField(auto_now=True)
    post_datetime = models.DateTimeField('快递时间', null=True)
    post_channel = models.CharField('快递方式', max_length=30, null=True)
    post_number = models.CharField('快递单号', max_length=30, null=True)
    status = models.CharField(max_length=30, choices=STATUS, null=True)
    img = models.ImageField('学分转换结果证明', upload_to='project/result/img/', null=True)

    class Meta:
        db_table = 'project_result'