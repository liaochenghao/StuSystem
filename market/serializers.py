# coding: utf-8
from common.models import SalesMan
from market.models import Channel
from rest_framework import serializers
from utils.functions import get_long_qr_code


class SalesManSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesMan
        fields = ['id', 'name']


class ChannelSerializer(serializers.ModelSerializer):
    # sales_man = SalesManSerializer()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'plan_date', 'sales_man', 'plan_student_number', 'plan_file_student_number',
                  'plan_payed_student_number', 'create_time', 'qr_code']
        read_only_fields = ['qr_code']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.qr_code = get_long_qr_code('channel_id_%s' % instance.id)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sales_man'] = SalesManSerializer(instance=instance.sales_man).data
        return data