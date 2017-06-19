# coding: utf-8
from django.db import models
from authentication.models import User


class Coupon(models.Model):
    """
    优惠券model
    """
    code = models.CharField("优惠码", max_length=30)
    amount = models.DecimalField("优惠金额")
    info = models.CharField("优惠说明", max_length=30)
    create_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_num = models.IntegerField('优惠券最大数')
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = "coupon"


class UserCoupon(models.Model):
    """
    User和优惠券关系表
    """
    user = models.ForeignKey(User)
    coupon = models.ForeignKey(Coupon)

    class Meta:
        db_table = "user_coupon"
        