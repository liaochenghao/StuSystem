# coding: utf-8
from django.db import models


class CampusType(models.Model):
    """
    校区类型表
    """
    title = models.CharField('校区类型', max_length=30)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        db_table = "campus_type"


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