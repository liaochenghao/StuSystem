# coding: utf-8
from django.db import models
from authentication.models import User
from utils.mysql_db import execute_sql


class CampusType(models.Model):
    """
    校区类型表
    """
    title = models.CharField('暑校类型', max_length=30)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        db_table = "campus_type"

    def __str__(self):
        return self.title


class Campus(models.Model):
    """
    校区信息表
    """
    name = models.CharField('校区名称', max_length=30)
    campus_type = models.ForeignKey(CampusType)
    info = models.CharField("校区描述", max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now=True)

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
    address = models.CharField('上课地点', max_length=30, null=True)
    info = models.CharField('项目描述', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    apply_fee = models.FloatField('申请费', null=True)
    course_num = models.IntegerField('课程数')

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name

    @property
    def current_applyed_number(self):
        data = execute_sql('select * from stu_system.order o where o.project_id=%d group by o.user_id' % self.id)
        return len(data)

    @property
    def current_payed_number(self):
        data = execute_sql('select * from stu_system.order o where o.project_id=%d and o.status="CONFIRMED" '
                           'group by o.user_id' % self.id)
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
    start_time = models.DateTimeField('上课开始时间')
    end_time = models.DateTimeField('上课结束时间')
    address = models.CharField('上课地点', max_length=30)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    syllabus = models.FileField('课程大纲', upload_to='course/syllabus', null=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name


class ProjectResult(models.Model):
    """用户学分转换"""
    STATUS = (
        ('POSTED', '成绩单已寄出'),
        ('RECEIVED', '学校已收到'),
        ('SUCCESS', '学分转换成功')
    )
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now=True)
    post_date = models.DateField('快递日期', null=True)
    post_channel = models.CharField('快递方式', max_length=30, null=True)
    post_number = models.CharField('快递单号', max_length=30, null=True)
    status = models.CharField(max_length=30, choices=STATUS, null=True)
    img = models.ImageField('学分转换结果证明', upload_to='project/result/img/', null=True)

    class Meta:
        db_table = 'project_result'
        unique_together = ['user', 'project']