# coding: utf-8
import random, string
from rest_framework import serializers
from course.models import Project, Campus, CampusType, Course, UserCourse
from order.models import Order


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
        fields = ['id', 'campus', 'name', 'start_date', 'end_date', 'address', 'info', 'create_time',
                  'apply_fee', 'course_num']

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


class CurrentCourseProjectSerializer(serializers.Serializer):
    project = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate(self, attrs):
        if not Project.objects.filter(id=attrs['project']).exists():
            raise serializers.ValidationError('项目不存在')

        if not Order.objects.filter(user_id=attrs['user'], project_id=attrs['project'],
                                    ).exists():
            raise serializers.ValidationError('订单不存在')

        if not Order.objects.filter(user_id=attrs['user'], project_id=attrs['project'],
                                    status='PAYED').exists():
            raise serializers.ValidationError('订单未支付')
        return attrs


class CreateUserCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'project', 'user']

    def validate(self, attrs):
        if not Order.objects.filter(user=attrs['user'], project=attrs['project'],
                                    ).exists():
            raise serializers.ValidationError('订单不存在')

        if not Order.objects.filter(user=attrs['user'], project=attrs['project'],
                                    status='PAYED').exists():
            raise serializers.ValidationError('订单未支付')

        if UserCourse.objects.filter(user=attrs['user'], project=attrs['project'],
                                     course=attrs['course']).exists():
            raise serializers.ValidationError('已选该课程，不能重复选择')
        return attrs