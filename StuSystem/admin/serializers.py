# coding: utf-8
import json

from admin.functions import get_channel_info
from admin.models import PaymentAccountInfo
from authentication.functions import auto_assign_sales_man
from common.models import SalesMan
from coupon.models import UserCoupon
from source.models import Project, Campus, Course
from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from authentication.models import UserInfo, UserInfoRemark, StudentScoreDetail, User
from order.models import UserCourse, Order
from order.serializers import OrderSerializer
from operate_history.serializers import OrderOperateHistorySerializer
from utils.serializer_fields import VerboseChoiceField
from utils.functions import get_long_qr_code


class AdminPaymentAccountInfoSerializer(serializers.ModelSerializer):
    payment = VerboseChoiceField(PaymentAccountInfo.PAYMENT)
    currency = VerboseChoiceField(PaymentAccountInfo.CURRENCY)

    class Meta:
        model = PaymentAccountInfo
        fields = ['id', 'account_number', 'account_name', 'opening_bank', 'payment', 'currency', 'swift_code']


class UserInfoSerializer(serializers.ModelSerializer):
    """UserInfo列表Serializer"""
    last_login = serializers.DateTimeField(source='user.last_login')

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'cschool', 'last_login', 'wechat']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        personal_file = all([instance.first_name, instance.last_name, instance.gender, instance.id_number,
                             instance.major, instance.graduate_year, instance.gpa])  # 判断用户是否已建档
        data['personal_file'] = '已建档' if personal_file else '未建档'
        data['channel'] = get_channel_info(instance)
        return data


class UserInfoRemarkSerializer(serializers.ModelSerializer):
    """添加用户信息备注Serializer"""
    user_info = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), write_only=True)

    class Meta:
        model = UserInfoRemark
        fields = ['id', 'remark', 'user_info', 'create_time']


class RetrieveUserInfoSerializer(serializers.ModelSerializer):
    """用户信息详情Serializer"""
    user_info_remark = UserInfoRemarkSerializer(many=True)
    gender = VerboseChoiceField(choices=UserInfo.GENDER)

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'first_name', 'last_name', 'gender', 'id_number', 'wechat',
                  'cschool', 'wcampus', 'major', 'graduate_year', 'gpa', 'user_info_remark']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_coupon = None
        if UserCoupon.objects.filter(user=instance.user, status='TO_USE').exists():
            user_coupon = UserCoupon.objects.filter(user=instance.user, status='TO_USE').values(
                'coupon__id', 'user', 'coupon__info', 'coupon__start_time', 'coupon__end_time', 'coupon__coupon_code', 'coupon__amount')
            for item in user_coupon:
                item['id'] = item.pop('coupon__id')
                item['info'] = item.pop('coupon__info')
                item['start_time'] = item.pop('coupon__start_time')
                item['end_time'] = item.pop('coupon__end_time')
                item['coupon_code'] = item.pop('coupon__coupon_code')
                item['amount'] = item.pop('coupon__amount')

        data['user_coupon'] = user_coupon
        data['channel'] = get_channel_info(instance)
        try:
            data['wcampus'] = Campus.objects.filter(id__in=json.loads(instance.wcampus)).\
                values('id', 'name', 'info', 'create_time')
        except Exception as e:
            data['wcampus'] = None

        sales_man = auto_assign_sales_man(instance.user)
        if sales_man:
            data['sales_man'] = sales_man
        else:
            data['sales_man'] = None
        return data


class ConfirmCourseSerializer(serializers.ModelSerializer):
    status = VerboseChoiceField(choices=UserCourse.STATUS)

    class Meta:
        model = UserCourse
        fields = ['confirm_img', 'status', 'user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        project = Project.objects.filter(id=instance.project_id).first()
        course = Course.objects.filter(id=instance.course_id).first()
        data['project'] = {
            'id': project.id,
            'name': project.name
        } if project else None

        data['course'] = {
            'id': course.id,
            'name': course.name,
            'course_code': course.course_code
        } if course else None
        return data


class CourseScoreSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='course.project.name')
    course_code = serializers.CharField(source='course.course_code')
    start_time = serializers.DateTimeField(source='course.start_time')
    end_time = serializers.DateTimeField(source='course.end_time')

    class Meta:
        model = UserCourse
        fields = ['project_name', 'course_code', 'start_time', 'end_time', 'score', 'score_grade', 'user', 'order',
                  'course']


class StudentScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScoreDetail
        fields = ['user', 'department', 'phone', 'country', 'post_code', 'address']


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


class SalesManSerializer(serializers.ModelSerializer):
    qr_code = Base64ImageField()
    # qr_code = serializers.ImageField()

    class Meta:
        model = SalesMan
        fields = ['id', 'name', 'wechat', 'email', 'qr_code']


class AdminCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'name', 'credit']


class AdminUserCourseSerializer(serializers.ModelSerializer):
    course = AdminCourseSerializer(read_only=True)
    status = VerboseChoiceField(UserCourse.STATUS)

    def validate(self, attrs):
        if self.instance:
            if self.instance.status == 'TO_UPLOAD' and (
                    attrs.get('status') == 'PASS' or attrs.get('status') == 'NOPASS'):
                raise serializers.ValidationError('用户还未上传审课图片，不能更改审课状态为通过或不通过')
            if self.instance.status == 'TO_UPLOAD' and attrs.get('status') == 'TO_CONFIRM':
                raise serializers.ValidationError('用户还未上传审课图片，管理员不能更改状态为待审核')
        return attrs

    class Meta:
        model = UserCourse
        fields = ['id', 'order', 'course', 'score', 'score_grade', 'reporting_time', 'confirm_img', 'status']
        read_only_fields = ['order', 'confirm_img']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_info = UserInfo.objects.filter(user=instance.user).values('user_id', 'name', 'email', 'wechat').first()
        user_info['user'] = user_info.pop('user_id')
        data['user_info'] = user_info
        return data


class AdminCreateUserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'order', 'user']

    def validate(self, attrs):
        if not Order.objects.filter(user=attrs['user'], project=attrs['order'].project,
                                    ).exists():
            raise serializers.ValidationError('订单不存在')

        if attrs['order'] == 'TO_CONFIRM':
            raise serializers.ValidationError('订单已支付但未确认, 请联系管理员确认订单')

        if attrs['order'] == 'TO_PAY':
            raise serializers.ValidationError('订单尚未支付')

        if UserCourse.objects.filter(order=attrs['order']).count() >= int(attrs['order'].course_num):
            raise serializers.ValidationError('已达到订单最大选课数，不能再继续选课')

        if UserCourse.objects.filter(user=attrs['user'], order=attrs['order'],
                                     course=attrs['course']).exists():
            raise serializers.ValidationError('已选该课程，不能重复选择')
        return attrs


class AddUserCourseScoreSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    score = serializers.IntegerField()
    score_grade = serializers.CharField()


class ConfirmUserCourseSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    status = VerboseChoiceField(choices=UserCourse.STATUS)


class AdminCourseCreditSwitchSerializer(serializers.ModelSerializer):
    """学分转换"""
    credit_switch_status = VerboseChoiceField(choices=UserCourse.CREDIT_SWITCH_STATUS)

    class Meta:
        model = UserCourse
        fields = ['id', 'post_datetime', 'post_channel', 'post_number', 'credit_switch_status', 'switch_img']
        read_only_fields = ['switch_img']

    def validate(self, attrs):
        if self.instance:
            if not (self.instance.confirm_img and (attrs.get('status') == 'PASS')):
                raise serializers.ValidationError('审课证明未确认，不能更改学分转换状态')
            if not self.instance.switch_img:
                raise serializers.ValidationError('学分转换证明图片未上传，不能更改学分转换状态')
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_info = UserInfo.objects.filter(user=instance.user).values('id', 'name', 'email', 'wechat').first()
        data['user_info'] = user_info
        return data


class ChildUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = VerboseChoiceField(User.ROLE)

    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'username', 'is_active', 'qr_code', 'role']
        read_only_fields = ['qr_code']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        instance = super().create(validated_data)
        qr_code = get_long_qr_code('child_user_%s' % instance.id)
        instance.qr_code = qr_code
        instance.save()
        return instance


class AdminOrderSerializer(OrderSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['operation_history'] = OrderOperateHistorySerializer(instance.orderoperatehistory_set.all(), many=True).data
        return data