# coding: utf-8
from rest_framework import serializers
from admin.models import PaymentAccountInfo
from authentication.models import UserInfo
from utils.serializer_fields import VerboseChoiceField


class PaymentAccountInfoSerializer(serializers.ModelSerializer):
    payment = VerboseChoiceField(PaymentAccountInfo.PAYMENT)

    class Meta:
        model = PaymentAccountInfo
        fields = ['id', 'account_number', 'account_name', 'opening_bank', 'payment']


class UserInfoSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(source='user.last_login')

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'cschool', 'last_login']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        personal_file = any([instance.first_name, instance.last_name, instance.gender, instance.id_number,
                             instance.major, instance.graduate_year, instance.gpa])  # 判断用户是否已建档
        data['personal_file'] = '已建档' if personal_file else '未建档'
        return data