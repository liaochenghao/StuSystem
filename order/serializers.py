# coding: utf-8
import json
from rest_framework import serializers
from order.models import Order
from coupon.models import UserCoupon
from course.serializers import ProjectSerializer
from utils.serializer_fields import VerboseChoiceField


class OrderSerializer(serializers.ModelSerializer):
    coupon_list = serializers.ListField(write_only=True)
    currency = VerboseChoiceField(choices=Order.CURRENCY)
    payment = VerboseChoiceField(choices=Order.PAYMENT)
    status = VerboseChoiceField(choices=Order.STATUS, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'project', 'currency', 'payment', 'create_time', 'status', 'standard_fee',
                  'pay_fee', 'coupon_list']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        UserCoupon.objects.filter(user=user, coupon__id__in=validated_data['coupon_list']).update(used=True)
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance=instance.project).data
        return data