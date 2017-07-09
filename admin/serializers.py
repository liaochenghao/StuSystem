# coding: utf-8
from rest_framework import serializers
from admin.models import PaymentAccountInfo
from course.models import Project, Campus
from order.models import UserCourse, Order
from authentication.models import UserInfo, UserInfoRemark, UserScoreDetail
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


class UserScoreDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserScoreDetail
        fields = ['user', 'department', 'phone', 'country', 'post_code', 'address']


class AdminProjectSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name')

    class Meta:
        model = Project
        fields = ['id', 'campus_name', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['applyed_num'] = instance.order_set.all().count()
        data['payed_num'] = instance.order_set.filter(status__in=['PAYED', 'CONFIRMED']).count()
        return data


class ProjectOverViewSerializer(serializers.ModelSerializer):
    applyed_number = serializers.IntegerField(source='current_applyed_number')
    payed_number = serializers.IntegerField(source='current_payed_number')

    class Meta:
        model = Project
        fields = ['id', 'name', 'applyed_number', 'payed_number']


class CampusOverViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_set'] = ProjectOverViewSerializer(Project.objects.filter(campus=instance), many=True).data
        return data