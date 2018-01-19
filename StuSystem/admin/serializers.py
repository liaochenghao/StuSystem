# coding: utf-8
import datetime
import json

from StuSystem import settings
from admin.functions import get_channel_info, order_confirmed_template_message, create_course_template_message
from admin.models import PaymentAccountInfo
from authentication.functions import auto_assign_sales_man
from common.models import SalesMan, FirstLevel, SecondLevel, SalesManUser
from coupon.models import UserCoupon
from operate_history.functions import HistoryFactory
from source.models import Project, Campus, Course, CourseProject
from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, exceptions

from authentication.models import UserInfo, UserInfoRemark, StudentScoreDetail, User
from order.models import UserCourse, Order, ShoppingChart
from order.serializers import OrderSerializer
from utils.serializer_fields import VerboseChoiceField
from micro_service.service import WeixinServer


class AdminPaymentAccountInfoSerializer(serializers.ModelSerializer):
    payment = VerboseChoiceField(PaymentAccountInfo.PAYMENT)
    currency = VerboseChoiceField(PaymentAccountInfo.CURRENCY)

    class Meta:
        model = PaymentAccountInfo
        fields = ['id', 'account_number', 'account_name', 'opening_bank', 'payment', 'currency', 'swift_code']


class UserInfoSerializer(serializers.ModelSerializer):
    """UserInfo列表Serializer"""
    last_login = serializers.DateTimeField(source='user.last_login')
    status = serializers.DictField(source='student_status')

    class Meta:
        model = UserInfo
        fields = ['user_id', 'name', 'email', 'cschool', 'last_login', 'wechat', 'status']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['channel'] = get_channel_info(instance.user)
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
        data['channel'] = get_channel_info(instance.user)
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
        fields = ['confirm_img', 'status', 'user', 'order']

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

    class Meta:
        model = UserCourse
        fields = ['score', 'score_grade', 'user', 'order', 'course', 'id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course'] = {'id': instance.course.id, 'course_code': instance.course.course_code,
                          'name': instance.course.name}
        data['project'] = {'id': instance.project.id, 'name': instance.project.name}
        return data


class StudentScoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentScoreDetail
        fields = ['id', 'user', 'department', 'phone', 'country', 'post_code', 'address']


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
    status = VerboseChoiceField(UserCourse.STATUS, required=False)

    def validate(self, attrs):
        if self.instance:
            if self.instance.status == 'TO_UPLOAD':
                raise serializers.ValidationError('用户还未上传审课图片，不能填入成绩')
            if self.instance.status == 'TO_CONFIRM':
                raise serializers.ValidationError('未审核学生上传的审课图片，不能填入成绩')
            if self.instance.status == 'NOPASS':
                raise serializers.ValidationError('学生的审课图片不通过，不能填入成绩')
        return attrs

    class Meta:
        model = UserCourse
        fields = ['id', 'order', 'course', 'score', 'score_grade', 'reporting_time', 'confirm_img', 'status']
        read_only_fields = ['order', 'confirm_img']

    def update(self, instance, validated_data):
        if validated_data.get('score') or validated_data.get('score_grade'):
            validated_data.update({'reporting_time': datetime.datetime.now()})
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_info = UserInfo.objects.filter(user=instance.user).values('user_id', 'name', 'email', 'wechat').first()
        user_info['user'] = user_info.pop('user_id')
        data['user_info'] = user_info
        return data


class AdminCreateUserCourseSerializer(serializers.ModelSerializer):
    """管理员为学生选课"""
    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'order', 'user', 'project']

    def validate(self, attrs):
        if attrs['order'] == 'TO_CONFIRM':
            raise serializers.ValidationError('订单已支付但未确认, 请联系管理员确认订单')

        if attrs['order'] == 'TO_PAY':
            raise serializers.ValidationError('订单尚未支付')

        chart = ShoppingChart.objects.filter(orderchartrelation__order=attrs['order'], project=attrs['project']).first()

        if not chart:
            raise serializers.ValidationError('未找到有效的chart')

        if UserCourse.objects.filter(order=attrs['order'], project=attrs['project'], user=attrs['user']).count() >= chart.course_num:
            raise serializers.ValidationError('已达到订单最大选课数，不能再继续选课')

        if UserCourse.objects.filter(user=attrs['user'], order=attrs['order'], project=attrs['project'],
                                     course=attrs['course']).exists():
            raise serializers.ValidationError('已选该课程，不能重复选择')
        return attrs

    def create_course_notice(self, validated_data):
        openid = validated_data['user'].username
        user_info = UserInfo.objects.filter(user=validated_data['user']).first()
        user_name = '%s%s' % (user_info.first_name, user_info.last_name) if (user_info.first_name and user_info.last_name) \
            else user_info.wx_name
        sales_man_user = SalesManUser.objects.filter(user=validated_data['user']).first()
        sales_man_name = '管理员' if (not sales_man_user) else sales_man_user.sales_man.name
        course_name = validated_data['course'].name
        course_project = CourseProject.objects.filter(course=validated_data['course'], project=validated_data['project']).first()
        address = course_project.address if course_project else '上课地点待定'
        course_time = '%s至%s' % (course_project.start_time.strftime('%Y-%m-%d'),
                                 course_project.end_time.strftime('%Y-%m-%d')) if \
            (course_project.start_time and course_project.end_time) else '上课时间待定'
        project_name = validated_data['project'].name
        create_course_template_message(openid=openid, user_name=user_name, sales_man_name=sales_man_name,
                                       project_name=project_name, course_name=course_name, course_time=course_time, address=address)

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.create_course_notice(validated_data)
        return instance


class AdminAvailableCoursesSerializer(serializers.Serializer):
    """管理员为学生选课可以选择的课程"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())


class ConfirmUserCourseSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    status = VerboseChoiceField(choices=UserCourse.STATUS)

    def validate(self, attrs):
        user_course = UserCourse.objects.filter(user=attrs['user'], course=attrs['course'],
                                                project=attrs['project'], order=attrs['order']).first()
        if not user_course:
            raise serializers.ValidationError('参数传入有误, 请检查传入参数')

        if user_course.status == 'PASS':
            raise serializers.ValidationError('审课已经通过')

        if user_course.status == 'TO_UPLOAD':
            raise serializers.ValidationError('该用户还未上传审课图片，不能更改审课状态')

        return attrs


class AdminCourseCreditSwitchSerializer(serializers.ModelSerializer):
    """学分转换"""
    credit_switch_status = VerboseChoiceField(choices=UserCourse.CREDIT_SWITCH_STATUS)

    class Meta:
        model = UserCourse
        fields = ['id', 'post_datetime', 'post_channel', 'post_number', 'credit_switch_status', 'switch_img']

    def validate(self, attrs):
        if self.instance:
            if self.instance.status == 'TO_UPLOAD':
                raise serializers.ValidationError('用户还未上传审课图片，更新学分转换进度')
            if self.instance.status == 'TO_CONFIRM':
                raise serializers.ValidationError('未审核学生上传的审课图片，更新学分转换进度')
            if self.instance.status == 'NOPASS':
                raise serializers.ValidationError('学生的审课图片不通过，更新学分转换进度')
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_info = UserInfo.objects.filter(user=instance.user).values('id', 'name', 'email', 'wechat').first()
        data['user_info'] = user_info
        data['switch_img'] = '%s%s%s' % (settings.DOMAIN, settings.MEDIA_URL, instance.switch_img) if instance.switch_img else None
        data['course'] = {'id': instance.course.id, 'name': instance.course.name,
                          'course_code': instance.course.course_code}
        data['project'] = {'id': instance.project.id, 'name': instance.project.name}
        return data


class AdminUserCourseAddressSerializer(serializers.ModelSerializer):
    """成绩单寄送地址Serializer"""
    class Meta:
        model = UserCourse
        fields = ['id', 'project', 'course']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = {
            'id': instance.project.id,
            'name': instance.project.name
        }
        data['course'] = {
            'id': instance.course.id,
            'course_code': instance.course.course_code,
            'name': instance.course.name
        }
        chart = ShoppingChart.objects.filter(project=instance.project, orderchartrelation__order=instance.order).first()
        if chart is None:
            raise serializers.ValidationError('usr_course_id: %s' % instance.id)
        data['student_score_detail'] = {
            'id': chart.stu_score_detail.id if chart.stu_score_detail else None,
            'department': chart.stu_score_detail.department if chart.stu_score_detail else '无',
            'phone': chart.stu_score_detail.phone if chart.stu_score_detail else '无',
            'country': chart.stu_score_detail.country if chart.stu_score_detail else '无',
            'post_code': chart.stu_score_detail.post_code if chart.stu_score_detail else '无',
            'address': chart.stu_score_detail.address if chart.stu_score_detail else '无'
        }
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
        qr_code = WeixinServer.get_forever_qr_code(action_name='QR_LIMIT_SCENE', scene_id='child_user_%s' % instance.id)
        instance.qr_code = qr_code
        instance.save()
        return instance


class AdminOrderSerializer(OrderSerializer):

    def notice_to_user(self, instance, confirm_status, confirm_remark):
        openid = instance.user.username
        user_info = UserInfo.objects.filter(user=instance.user).first()
        name = '%s%s' % (user_info.first_name, user_info.last_name) if (user_info.first_name and user_info.last_name) \
            else user_info.wx_name
        order_confirmed_template_message(openid=openid, name=name, confirm_status=confirm_status, remark=confirm_remark)
        return

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('status') == 'CONFIRM_FAILED' and not attrs.get('remark'):
            raise serializers.ValidationError('订单审核失败时，必须填写失败原因')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'CONFIRMED':
            status = 'CONFIRMED'
            remark = '订单支付成功，已确认'
            confirm_status = '订单支付成功'
            confirm_remark = '您的订单审核成功，请联系您的课程顾问，开始选课吧！'

        elif validated_data.get('status') == 'CONFIRM_FAILED':
            status = 'CONFIRM_FAILED'
            remark = '订单支付失败，原因为: %s' % validated_data.get('remark')
            confirm_status = '订单支付失败'
            confirm_remark = '很抱歉，您的订单审核失败，失败原因为: %s' % validated_data.get('remark')
        else:
            raise exceptions.ValidationError('请传入正确的status参数')
        if instance.status != 'TO_CONFIRM':
            raise exceptions.ValidationError('仅能操作待确认状态下的订单')
        if instance.status != 'TO_CONFIRM':
            raise exceptions.ValidationError('仅能操作待确认下的订单')
        instance.status = status
        instance.save()
        if instance.coupon_list:
            # 如果使用了优惠券，更新优惠券的状态
            coupon_list = json.loads(instance.coupon_list)
            UserCoupon.objects.filter(user=instance.user, coupon__id__in=coupon_list).update(
                status='USED' if status == 'CONFIRMED' else 'TO_USE')
        self.notice_to_user(instance, confirm_status, confirm_remark)
        HistoryFactory.create_record(operator=self.context['request'].user, source=instance, key='UPDATE', remark=remark,
                                     source_type='ORDER')
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['operation_history'] = HistoryFactory.read_records(source=instance, source_type='ORDER')
        for chart in data['charts']:
            current_course_num = instance.usercourse_set.all().filter(
                user=instance.user, project_id=chart['project']['id'], order=instance).count()
            chart['current_course_num'] = current_course_num
        user_coupons = UserCoupon.objects.filter(coupon_id__in=json.loads(instance.coupon_list), user=instance.user) if instance.coupon_list else None
        data['coupons_info'] = [{'id': user_coupon.coupon.id, 'amount': user_coupon.coupon.amount,
                                 'coupon_code': user_coupon.coupon.coupon_code, 'info': user_coupon.coupon.info}
                                for user_coupon in user_coupons] if user_coupons else None
        return data


class SecondLevelSerializer(serializers.ModelSerializer):
    """二级菜单Serializer"""
    class Meta:
        model = SecondLevel
        fields = ['id', 'name', 'key', 'icon']


class FirstLevelSerializer(serializers.ModelSerializer):
    """一级菜单serializer"""

    class Meta:
        model = FirstLevel
        fields = ['id', 'name', 'key']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        second_levels = SecondLevel.objects.filter(secondlevelrole__role=self.context['request'].user.role,
                                                   firstsecondrelation__first=instance).order_by('id')
        data['second_levels'] = SecondLevelSerializer(second_levels, many=True).data
        return data