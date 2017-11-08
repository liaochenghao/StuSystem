# coding: utf-8
from rest_framework import serializers

from course.models import Campus, CampusType


class CampusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusType
        fields = ['id', 'title', 'create_time']


class CampusSerializer(serializers.ModelSerializer):
    campus_type = CampusTypeSerializer()

    class Meta:
        model = Campus
        fields = ['id', 'campus_type', 'name', 'info', 'create_time']