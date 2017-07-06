# coding: utf-8
from rest_framework import serializers
from order.models import Order, OrderCoupon, OrderPayment
from course.models import ProjectCourseFee
from course.serializers import ProjectSerializer
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer
from coupon.models import Coupon
from utils.serializer_fields import VerboseChoiceField


class OrderSerializer(serializers.ModelSerializer):
    currency = VerboseChoiceField(choices=Order.CURRENCY)
    payment = VerboseChoiceField(choices=Order.PAYMENT)
    status = VerboseChoiceField(choices=Order.STATUS, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'project', 'currency', 'payment', 'create_time', 'status',
                  'course_num', 'standard_fee', 'pay_fee']
        read_only_fields = ['user', 'pay_fee', 'standard_fee']

    def validate(self, attrs):
        if attrs['course_num'] > attrs['project'].course_num:
            raise serializers.ValidationError('所选课程数大于项目最大课程数, 项目最大选课数{}'.format(attrs['project'].course_num))
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        course_fee = ProjectCourseFee.objects.filter(project=validated_data['project'],
                                                     course_number=validated_data['course_num']).first()
        validated_data['standard_fee'] = validated_data['project'].apply_fee + course_fee.course_fee if course_fee else 0
        validated_data['user'] = user
        order = super().create(validated_data)
        return order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance=instance.project).data
        payment_info = PaymentAccountInfo.objects.filter(payment=instance.payment).first()
        data['payment_info'] = PaymentAccountInfoSerializer(payment_info).data if payment_info else None
        return data


class OrderPaymentSerializer(serializers.ModelSerializer):
    coupon_list = serializers.ListField(write_only=True, allow_empty=True)

    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'account_number', 'account_name', 'opening_bank', 'pay_date', 'coupon_list']

    def create(self, validated_data):
        order_coupon = []
        coupon_list = validated_data.pop('coupon_list')
        pay_fee = validated_data['order'].standard_fee
        if coupon_list:
            amount = Coupon.objects.filter(id__in=coupon_list).values_list('amount', flat=True)
            for item in coupon_list:
                order_coupon.append(OrderCoupon(**{'order': validated_data['order'], 'coupon_id': item}))
            OrderCoupon.objects.bulk_create(order_coupon)

            for item in amount:
                pay_fee -= item
        validated_data['order'].pay_fee = pay_fee if pay_fee >= 0 else 0
        validated_data['order'].save()
        return super().create(validated_data)