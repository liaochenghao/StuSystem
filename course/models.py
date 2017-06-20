# coding: utf-8
from django.db import models


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

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name