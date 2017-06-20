# coding: utf-8
from rest_framework import serializers
from order.models import Order
from course.serializers import ProjectSerializer
from utils.serializer_fields import VerboseChoiceField


class OrderSerializer(serializers.ModelSerializer):
    currency = VerboseChoiceField(choices=Order.CURRENCY)
    payment = VerboseChoiceField(choices=Order.PAYMENT)
    status = VerboseChoiceField(choices=Order.STATUS, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'project', 'currency', 'payment', 'create_time', 'status', 'standard_fee', 'pay_fee']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance=instance.project).data
        return data