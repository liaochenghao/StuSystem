# coding: utf-8
from rest_framework import serializers
from .models import Coupon, UserCoupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'amount', 'info', 'start_time', 'end_time',\
        			'max_num', 'create_time', 'is_active']

    def create_coupon(self):
    	coupon = Coupon(code=self.code, amount=self.amount, info=self.info, \
    		start_time=self.start_time, end_time=self.end_time, max_num=self.max_num, create_time=datetime.datetime.now(),\
    		is_active=self.is_active)
    	coupon.save()
    	return {'code': 0, 'msg': "请求成功"}


class UserCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoupon
        fields = ['id', 'user', 'coupon']

