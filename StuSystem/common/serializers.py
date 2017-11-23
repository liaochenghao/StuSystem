# coding: utf-8
from rest_framework import serializers
from source.models import Campus


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']