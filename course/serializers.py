# coding: utf-8
from rest_framework import serializers
from course.models import Project, Campus, CampusType


class CampusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusType
        fields = ['id', 'title', 'create_time']


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'campus_type', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['campus_type'] = CampusTypeSerializer(instance.campus_type).data
        return data


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'campus', 'name', 'start_date', 'end_date', 'address', 'max_num', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        serializer = CampusSerializer(instance=instance.campus)
        data['campus'] = serializer.data
        return data