# coding: utf-8
import datetime

from rest_framework import serializers
import random, string
from .models import Coupon, UserCoupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'coupon_code', 'amount', 'info', 'start_time', 'end_time',
                  'max_num', 'create_time', 'is_active']
        read_only_fields = ['coupon_code']

    def create(self, validated_data):
        validated_data['coupon_code'] = ''.join(random.sample(string.digits + string.ascii_uppercase, 10))
        return super().create(validated_data)


class UserCouponSerializer(serializers.ModelSerializer):
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.filter(is_active=True))

    class Meta:
        model = UserCoupon
        fields = ['id', 'user', 'coupon']

    def validate(self, attrs):
        if attrs['user'].role != 'STUDENT':
            raise serializers.ValidationError('仅能为学生用户分配优惠券')
        if not(attrs['coupon'].start_time.replace(tzinfo=None) < datetime.datetime.now() <
                   attrs['coupon'].end_time.replace(tzinfo=None)):
            raise serializers.ValidationError('优惠券已过期')
        if UserCoupon.objects.filter(coupon=attrs['coupon'], user=attrs['user']).exists():
            raise serializers.ValidationError('已经为该用户分配过该优惠券，不能重复分配')
        if UserCoupon.objects.filter(coupon=attrs['coupon']).count() >= attrs['coupon'].max_num:
            raise serializers.ValidationError('优惠券已超过最大数量，不能为该用户新增优惠券')
        return attrs

