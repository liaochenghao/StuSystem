# coding: utf-8
from rest_framework import serializers
from authentication.models import User, UserInfo
from operate_history.models import OrderOperateHistory
from utils.serializer_fields import VerboseChoiceField


class OperatorSerializer(serializers.ModelSerializer):
    """操作用户serializer"""
    role = VerboseChoiceField(choices=User.ROLE)

    class Meta:
        model = User
        fields = ['id', 'name', 'role']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role == 'STUDENT' and UserInfo.objects.filter(user=instance).exists():
            name = UserInfo.objects.get(user=instance).wx_name
            data['name'] = name
        return data


class OrderOperateHistorySerializer(serializers.ModelSerializer):
    """订单操作记录serializer"""
    operator = OperatorSerializer()

    class Meta:
        model = OrderOperateHistory
        fields = ['id', 'operator', 'create_time', 'source', 'remark']