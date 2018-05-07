# coding: utf-8
from common.models import SalesMan
from django.db import models

from authentication.models import User


class Channel(models.Model):
    """推广渠道"""
    name = models.CharField('推广名称', unique=True, max_length=30)
    plan_date = models.DateField('计划推广日期')
    sales_man = models.ForeignKey(SalesMan)
    plan_student_number = models.IntegerField('预计参加人数')
    plan_file_student_number = models.IntegerField('预计建档人数')
    plan_payed_student_number = models.IntegerField('预计缴费人数')
    phase_discount = models.CharField('阶段优惠说明', max_length=60, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    channel_url = models.CharField('推广二维码URL', max_length=255, null=True)
    qr_code = models.CharField('推广二维码', max_length=255, null=True)

    class Meta:
        db_table = 'market_channel'

    def __str__(self):
        return self.name


class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_channel'
