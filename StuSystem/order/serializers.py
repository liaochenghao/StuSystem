# coding: utf-8
import json

from StuSystem.settings import DOMAIN, MEDIA_URL
from admin.models import PaymentAccountInfo
from authentication.models import UserInfo, StudentScoreDetail
from common.models import SalesMan
from coupon.models import UserCoupon
from operate_history.functions import HistoryFactory
from source.models import ProjectCourseFee, Course
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from authentication.serializers import StudentScoreDetailSerializer
from source.serializers import ProjectSerializer
from order.models import Order, OrderPayment, UserCourse, ShoppingChart, OrderChartRelation
from utils.serializer_fields import VerboseChoiceField


class PaymentAccountInfoSerializer(serializers.ModelSerializer):
    """支付账号serializer"""
    payment = VerboseChoiceField(PaymentAccountInfo.PAYMENT)
    currency = VerboseChoiceField(PaymentAccountInfo.CURRENCY)

    class Meta:
        model = PaymentAccountInfo
        fields = ['id', 'account_number', 'account_name', 'opening_bank', 'payment', 'currency', 'swift_code']


class OrderSerializer(serializers.ModelSerializer):
    """订单的serializer"""
    currency = VerboseChoiceField(choices=Order.CURRENCY)
    payment = VerboseChoiceField(choices=Order.PAYMENT)
    status = VerboseChoiceField(choices=Order.STATUS, required=False)
    coupon_list = serializers.ListField(write_only=True, required=False)
    chart_ids = serializers.ListField(write_only=True, child=serializers.IntegerField())

    class Meta:
        model = Order
        fields = ['id', 'user', 'chart_ids', 'currency', 'payment', 'create_time', 'modified_time', 'status',
                  'standard_fee', 'pay_fee', 'remark', 'coupon_list']
        read_only_fields = ['user', 'pay_fee', 'standard_fee']

    def validate(self, attrs):
        if not self.instance:
            chart_ids = attrs['chart_ids']
            for chart_id in chart_ids:
                if not ShoppingChart.objects.filter(id=chart_id, status='NEW').exists():
                    raise serializers.ValidationError('无效的chart_id: %s，请检查传入参数' % chart_id)
            if attrs.get('coupon_list'):
                for coupon_id in attrs['coupon_list']:
                    if not UserCoupon.objects.filter(user=self.context['request'].user, coupon_id=coupon_id, status='TO_USE').exists():
                        raise serializers.ValidationError('无效的优惠券, coupon_id: %s' % coupon_id)

            if Order.objects.filter(user=self.context['request'].user,
                                    status__in=['TO_PAY', 'TO_CONFIRM']).exists():
                raise serializers.ValidationError('有未完成的订单，不能创建新的订单')
        else:
            if self.instance.status == 'CANCELED':
                raise serializers.ValidationError('该订单已被取消，不能进行更新任何操作')
            if self.instance.status == 'TO_PAY':
                if attrs.get('status') == 'CONFIRMED':
                    raise serializers.ValidationError('用户尚未上传凭证，不能进行确认操作')
            if self.instance.status == 'TO_CONFIRM':
                if attrs.get('status') == 'CANCELED':
                    raise serializers.ValidationError('该订单已被支付，在管理员确定前不能取消')
            if self.instance.status == 'CONFIRMED':
                raise serializers.ValidationError('管理员已确认该订单，不能进行任何更新操作')
            if self.instance.status == 'CONFIRM_FAILED':
                raise serializers.ValidationError('管理员已确认订单支付认证失败，不能进行任何更新操作')
        return attrs

    def create(self, validated_data):
        coupon_list = validated_data.pop('coupon_list', None)
        chart_ids = validated_data.pop('chart_ids')
        user = self.context['request'].user
        standard_fee = sum([item.course_fee for item in ShoppingChart.objects.filter(
            id__in=chart_ids, status='NEW')])
        validated_data['standard_fee'] = standard_fee
        validated_data['pay_fee'] = standard_fee
        validated_data['user'] = user
        if coupon_list:
            validated_data['coupon_list'] = json.dumps(coupon_list)
            # 计算优惠券费用
            coupon_list_fee = 0
            coupon_list_fee_values = UserCoupon.objects.filter(coupon_id__in=coupon_list).values_list('coupon__amount', flat=True)
            for item in coupon_list_fee_values:
                coupon_list_fee += item
            validated_data['pay_fee'] = standard_fee - coupon_list_fee if \
                (validated_data['standard_fee'] - coupon_list_fee) >= 0 else 0
        order = super().create(validated_data)
        if coupon_list:
            # 更新优惠券状态
            for coupon_id in coupon_list:
                if UserCoupon.objects.filter(user=user, coupon_id=coupon_id, status='TO_USE').exists():
                    UserCoupon.objects.filter(user=user, coupon_id=coupon_id, status='TO_USE').update(status='LOCKED')
        # 创建订单与商品关系
        order_chart = []
        for chart_id in chart_ids:
            order_chart.append(OrderChartRelation(order=order, chart_id=chart_id))
        OrderChartRelation.objects.bulk_create(order_chart)

        # 更新购物车
        ShoppingChart.objects.filter(id__in=chart_ids).update(status='ORDERED')
        # 操作记录
        HistoryFactory.create_record(operator=self.context['request'].user, source=order, key='CREATE', remark='创建了订单',
                                     source_type='ORDER')
        return order

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status in ['CONFIRMED', 'CONFIRM_FAILED'] and instance.coupon_list:
            coupon_list = json.loads(instance.coupon_list)
            if UserCoupon.objects.filter(user=instance.user, coupon_id__in=coupon_list).exists():
                UserCoupon.objects.filter(user=instance.user, coupon_id__in=coupon_list).update(status='USED')
        if instance.status == 'CANCELED' and instance.coupon_list:
            coupon_list = json.loads(instance.coupon_list)
            if UserCoupon.objects.filter(user=instance.user, coupon_id__in=coupon_list).exists():
                UserCoupon.objects.filter(user=instance.user, coupon_id__in=coupon_list).update(status='TO_USE')
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        charts = ShoppingChartSerializer(ShoppingChart.objects.filter(orderchartrelation__order=instance),
                                         many=True).data
        data['charts'] = charts
        payment_info = PaymentAccountInfo.objects.filter(payment=instance.payment).first()
        data['payment_info'] = PaymentAccountInfoSerializer(payment_info).data if payment_info else None
        order_payment = OrderPayment.objects.filter(order=instance).last()
        data['order_payed_info'] = OrderPaymentSerializer(order_payment).data if order_payment else None
        user_info = UserInfo.objects.get(user=instance.user)
        data['user'] = {
            'id': instance.user.id,
            'name': user_info.name
        }
        sales_man = SalesMan.objects.filter(salesmanuser__user=instance.user).first()
        data['sales_man'] = {'id': sales_man.id, 'name': sales_man.name} if sales_man else {}
        return data


class SimpleUserOrderSerializer(serializers.ModelSerializer):
    status = VerboseChoiceField(choices=Order.STATUS, required=False)

    class Meta:
        model = Order
        fields = ['id', 'create_time', 'status', 'standard_fee', 'pay_fee', 'remark']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        charts = ShoppingChartSerializer(ShoppingChart.objects.filter(orderchartrelation__order=instance),
                                         many=True).data
        data['charts'] = charts
        return data


class OrderCourseSerializer(serializers.ModelSerializer):
    """用于用户关联订单的审课"""
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'name', 'max_num', 'credit', 'professor', 'start_time', 'end_time',
                  'create_time', 'address', 'syllabus']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_course = UserCourse.objects.filter(course=instance).first()
        user_course_data = {
            'score': user_course.score,
            'score_grade': user_course.score_grade,
            'reporting_time': user_course.reporting_time,
            'confirm_img': user_course.confirm_img.path if user_course.confirm_img else None,
            'status': {
                'key': user_course.status,
                'verbose': dict(UserCourse.STATUS).get(user_course.status)
            }
        } if user_course else None
        data['confirm_course'] = user_course_data
        return data


class UserOrderCourseSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'project', 'currency', 'payment', 'create_time', 'status',
                  'course_num', 'standard_fee', 'pay_fee', 'project', 'remark']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_course = Course.objects.filter(usercourse__order=instance, usercourse__user=self.context['request'].user)
        user_course_data = OrderCourseSerializer(user_course, many=True).data if user_course else None
        data['user_course'] = user_course_data
        return data


class OrderPaymentSerializer(serializers.ModelSerializer):
    img = Base64ImageField()

    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'account_number', 'account_name', 'opening_bank', 'pay_date', 'img', 'amount']

    def create(self, validated_data):
        validated_data['order'].status = 'TO_CONFIRM'
        validated_data['order'].save()
        instance = super().create(validated_data)
        HistoryFactory.create_record(operator=self.context['request'].user, source=instance.order, key='UPDATE', remark='上传了订单支付信息',
                                     source_type='ORDER')
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['img'] = '%s%s%s' % (DOMAIN, MEDIA_URL, instance.img)
        return data


class ShoppingChartSerializer(serializers.ModelSerializer):
    """购物车"""
    stu_score_detail = serializers.PrimaryKeyRelatedField(queryset=StudentScoreDetail.objects.filter(is_active=True),
                                                          required=False)

    class Meta:
        model = ShoppingChart
        fields = ['id', 'project', 'course_num', 'course_fee', 'create_time', 'stu_score_detail']
        read_only_fields = ['course_fee']

    def validate(self, attrs):
        project = attrs['project']
        project_course_fee = ProjectCourseFee.objects.filter(project=project, project__is_active=True,
                                                             course_number=attrs['course_num']).first()
        if not project_course_fee:
            raise serializers.ValidationError('项目课程数量错误，请重新选择')
        attrs['course_fee'] = project_course_fee.course_fee + project.apply_fee
        attrs['user'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = ProjectSerializer(instance.project).data
        data['stu_score_detail'] = StudentScoreDetailSerializer(instance.stu_score_detail).data
        return data