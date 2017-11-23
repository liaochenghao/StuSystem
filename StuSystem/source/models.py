# coding: utf-8
from django.db import models


class Campus(models.Model):
    """
    校区信息表
    """
    name = models.CharField('校区名称', max_length=30)
    info = models.CharField("校区描述", max_length=100)
    network_course = models.BooleanField(default=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = "campus"

    def __str__(self):
        return self.name


class Project(models.Model):
    """项目表"""
    campus = models.ForeignKey(Campus)
    name = models.CharField('项目名称', max_length=30, null=True)
    start_date = models.DateField('开始时间')
    end_date = models.DateField('结束时间')
    address = models.CharField('项目地点', max_length=100, null=True)
    info = models.CharField('项目描述', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    apply_fee = models.FloatField('申请费', null=True)
    course_num = models.IntegerField('课程数')
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name

    @property
    def current_applyed_number(self):
        from order.models import Order
        data = Order.objects.filter(orderchartrelation__chart__project=self,
                                    status__in=['TO_PAY', 'TO_CONFIRM', 'CONFIRMED']).values_list('user_id', flat=True)
        return len(data)

    @property
    def current_payed_number(self):
        from order.models import Order
        data = Order.objects.filter(orderchartrelation__chart__project=self,
                                    status__in=['CONFIRMED']).values_list('user_id', flat=True)
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
    course_code = models.CharField('课程代码', max_length=30, unique=True)
    name = models.CharField('课程名称', max_length=255)
    max_num = models.IntegerField('最大容纳人数')
    credit = models.IntegerField('学分')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name


class CourseProject(models.Model):
    """课程与项目对应表"""
    project = models.ForeignKey(Project, verbose_name='项目名称')
    course = models.ForeignKey(Course, verbose_name='课程名称')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    professor = models.CharField('授课教授', max_length=30)
    start_time = models.DateField('上课开始时间')
    end_time = models.DateField('上课结束时间')
    address = models.CharField('上课地点', max_length=100)

    class Meta:
        db_table = 'course_project'
        unique_together = ['project', 'course']