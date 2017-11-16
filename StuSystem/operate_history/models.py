# coding: utf-8
from django.db import models
from authentication.models import User
from order.models import Order


class OperateHistory(models.Model):
    """操作记录"""
    OPERATE_KEY = (
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除')
    )
    operator = models.ForeignKey(User)
    key = models.CharField('操作类型', max_length=30, choices=OPERATE_KEY)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    source = None
    remark = models.CharField('备注', max_length=255)

    class Meta:
        abstract = True


class OrderOperateHistory(OperateHistory):
    """订单操作记录"""
    source = models.ForeignKey(Order)

    class Meta:
        db_table = 'order_operate_history'