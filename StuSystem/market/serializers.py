# coding: utf-8
from rest_framework import serializers

from common.models import SalesMan
from market.models import Channel
from micro_service.service import WeixinServer


class SalesManSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesMan
        fields = ['id', 'name']


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['id', 'name', 'plan_date', 'sales_man', 'plan_student_number', 'plan_file_student_number',
                  'plan_payed_student_number', 'create_time', 'qr_code']
        read_only_fields = ['qr_code']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.qr_code = WeixinServer.get_forever_qr_code(action_name='QR_LIMIT_SCENE',
                                                            scene_id='channel_id_%s' % instance.id)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sales_man'] = SalesManSerializer(instance=instance.sales_man).data
        return data