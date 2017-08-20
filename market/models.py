# coding: utf-8
from django.db import models
from common.models import SalesMan


class Channel(models.Model):
    name = models.CharField('推广名称', unique=True, max_length=30)
    plan_date = models.DateField('计划推广日期')
    sales_man = models.ForeignKey(SalesMan)
    plan_student_number = models.IntegerField('预计参加人数')
    plan_file_student_number = models.IntegerField('预计建档人数')
    plan_payed_student_number = models.IntegerField('预计缴费人数')
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    qr_code = models.CharField('推广二维码', max_length=255, null=True)

    class Meta:
        db_table = 'market_channel'

    def __str__(self):
        return self.name