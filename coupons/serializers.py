# coding: utf-8
from rest_framework import serializers
from coupons.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'amount', 'info', 'start_time', 'end_time']