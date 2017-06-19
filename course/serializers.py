# coding: utf-8
import random, string
from rest_framework import serializers
from course.models import Project, Campus, CampusType, Course


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


class CourseSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    course_code = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'project', 'course_code', 'name', 'max_num', 'credit', 'professor', 'start_time', 'end_time',
                  'create_time', 'address']

    def create(self, validated_data):
        validated_data['course_code'] = ''.join(random.sample(string.digits + string.ascii_uppercase, 10))
        return super().create(validated_data)