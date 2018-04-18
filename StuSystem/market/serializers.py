# coding: utf-8
from rest_framework import serializers

from admin.functions import make_qrcode
from authentication.models import User, UserInfo
from common.models import SalesMan
from market.models import Channel


class SalesManSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesMan
        fields = ['id', 'name']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'plan_date', 'sales_man', 'plan_student_number', 'plan_file_student_number',
                  'plan_payed_student_number', 'create_time', 'channel_url', 'qr_code', 'phase_discount']
        read_only_fields = ['qr_code']

    def create(self, validated_data):
        if self.context.get('request').user.channel_id:
            raise serializers.ValidationError('没有权限进行次操作')
        instance = super().create(validated_data)
        instance.qr_code, instance.channel_url = make_qrcode(instance.id)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sales_man'] = SalesManSerializer(instance=instance.sales_man).data
        query_set = UserInfo.objects.filter(user__channel_id=instance.id)
        data['all_stu_number'] = query_set.count()
        data['file_stu_number'] = query_set.exclude(student_status='NEW').count()
        data['payed_stu_number'] = query_set.filter(
            student_status__in=['TO_CHOOSE_COURSE', 'PICKUP_COURSE', 'TO_CONFIRMED', 'CONFIRMED_COURSE', 'AFTER_SCORE',
                                'SWITCH_CREDIT', 'SWITCHED_COURSE']).count()
        return data
