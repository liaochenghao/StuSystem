# coding: utf-8
from rest_framework import serializers
from admin.models import PaymentAccountInfo
from course.models import UserCourse
from authentication.models import UserInfo, UserInfoRemark
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


class UserInfoRemarkSerializer(serializers.ModelSerializer):
    user_info = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), write_only=True)

    class Meta:
        model = UserInfoRemark
        fields = ['id', 'remark', 'user_info', 'create_time']


class RetrieveUserInfoSerializer(serializers.ModelSerializer):
    user_info_remark = UserInfoRemarkSerializer(many=True)
    gender = VerboseChoiceField(choices=UserInfo.GENDER)

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'first_name', 'last_name', 'gender', 'id_number', 'wechat',
                  'cschool', 'major', 'graduate_year', 'gpa', 'user_info_remark']


class ConfirmCourseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='course.project.name')
    course_code = serializers.CharField(source='course.course_code')
    syllabus = serializers.CharField(source='course.syllabus')
    status = VerboseChoiceField(choices=UserCourse.STATUS)

    class Meta:
        model = UserCourse
        fields = ['project_name', 'course_code', 'syllabus', 'confirm_photo', 'status', 'user']


class CourseScoreSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='course.project.name')
    course_code = serializers.CharField(source='course.course_code')
    start_time = serializers.DateTimeField(source='course.start_time')
    end_time = serializers.DateTimeField(source='course.end_time')

    class Meta:
        model = UserCourse
        fields = ['project_name', 'course_code', 'start_time', 'end_time', 'score', 'score_grade', 'user']