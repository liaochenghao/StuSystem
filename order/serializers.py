# coding: utf-8
from rest_framework import serializers
from order.models import Order, OrderCoupon
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
        order_coupon = []
        coupon_list = []
        user = self.context['request'].user
        validated_data['user'] = user
        if validated_data.get('coupon_list'):
            coupon_list = validated_data.pop('coupon_list')
        order = super().create(validated_data)
        if coupon_list:
            for item in coupon_list:
                order_coupon.append(OrderCoupon(**{'order': order, 'coupon_id': item}))
            OrderCoupon.objects.bulk_create(order_coupon)
        return order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance=instance.project).data
        return data