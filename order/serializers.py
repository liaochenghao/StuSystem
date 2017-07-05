# coding: utf-8
from rest_framework import serializers
from order.models import Order, OrderCoupon, OrderPayment
from course.serializers import ProjectSerializer
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer
from utils.serializer_fields import VerboseChoiceField


class OrderSerializer(serializers.ModelSerializer):
    coupon_list = serializers.ListField(write_only=True, required=False)
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
        coupon_list = validated_data.pop('coupon_list')
        user = self.context['request'].user
        validated_data['user'] = user
        order = super().create(validated_data)
        if coupon_list:
            for item in coupon_list:
                order_coupon.append(OrderCoupon(**{'order': order, 'coupon_id': item}))
            OrderCoupon.objects.bulk_create(order_coupon)
        return order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance=instance.project).data
        payment_info = PaymentAccountInfo.objects.filter(payment=instance.payment).first()
        data['payment_info'] = PaymentAccountInfoSerializer(payment_info).data if payment_info else None
        return data


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'account_number', 'account_name', 'opening_bank', 'pay_date', 'img']