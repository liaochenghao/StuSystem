# coding: utf-8
from rest_framework import serializers

from admin.functions import make_qrcode
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
                  'plan_payed_student_number', 'create_time', 'channel_url', 'qr_code']
        read_only_fields = ['qr_code']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.qr_code, instance.channel_url = make_qrcode(instance.id)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sales_man'] = SalesManSerializer(instance=instance.sales_man).data
        return data
