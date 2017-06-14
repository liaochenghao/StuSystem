# coding: utf-8
from django.db import models
from common.models import Campus


class Project(models.Model):
    campus = models.ForeignKey(Campus)
    name = models.CharField('项目名称', max_length=30, null=True)
    start_date = models.DateTimeField('开始时间')
    end_date = models.DateTimeField('结束时间')
    address = models.CharField('上课地点', max_length=30, null=True)
    max_num = models.IntegerField('最大选课数量', null=True)
    info = models.CharField('项目描述', max_length=255, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'project'


class ProjectTuition(models.Model):
    project = models.ForeignKey(Project)
    apply_fee = models.FloatField('申请费', null=True)
    course_count = models.IntegerField('选课数', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'project_tuition'


class Course(models.Model):
    project = models.ForeignKey(Project)
    code = models.CharField('课程代码', max_length=30, null=True)
    name = models.CharField('课程名称', max_length=30, null=True)
    max_num = models.IntegerField('最大容纳人数', null=True)
    current_num = models.IntegerField('当前选课人数', null=True)
    credit = models.IntegerField('学分', null=True)
    professor = models.CharField('授课教授', max_length=30, null=True)
    course_time = models.DateTimeField('上课时间')
    course_addr = models.CharField('上课地点', max_length=30, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'course'