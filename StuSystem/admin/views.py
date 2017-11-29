# coding: utf-8
import datetime
import json

from admin.filters import UserInfoFilterSet, UserCourseFilterSet
from admin.models import PaymentAccountInfo
from authentication.models import UserInfo, StudentScoreDetail, User
from coupon.models import UserCoupon
from operate_history.functions import HistoryFactory
from permissions.base_permissions import BaseOperatePermission
from common.models import SalesMan, FirstLevel
from source.models import Campus, Course
from rest_framework import exceptions
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from admin.serializers import AdminPaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer, \
    UserInfoRemarkSerializer, ConfirmCourseSerializer, CourseScoreSerializer, StudentScoreDetailSerializer, \
    CampusOverViewSerializer, SalesManSerializer, AdminUserCourseSerializer, \
    AdminCourseCreditSwitchSerializer, AddUserCourseScoreSerializer, ConfirmUserCourseSerializer, ChildUserSerializer, \
    AdminCourseSerializer, AdminCreateUserCourseSerializer, AdminOrderSerializer, FirstLevelSerializer
from order.models import UserCourse, Order


class AccountInfoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """付款账号设置ViewSet"""
    queryset = PaymentAccountInfo.objects.all()
    serializer_class = AdminPaymentAccountInfoSerializer
    permission_classes = [BaseOperatePermission]


class UserInfoViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """用户信息ViewSet"""
    queryset = UserInfo.objects.all().exclude(user__role='ADMIN')
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilterSet
    permission_classes = [BaseOperatePermission]

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('many'):
            return UserInfoSerializer(*args, **kwargs)
        return RetrieveUserInfoSerializer(*args, **kwargs)

    def get_object(self):
        # pk 传过来的是user_id，需要转换为user_info
        user_id = self.kwargs.get('pk')
        try:
            user_info = self.queryset.get(user=user_id)
        except UserInfo.DoesNotExist:
            raise exceptions.NotFound('未找到user_info实例')
        return user_info

    @detail_route(['POST'])
    def add_remark(self, request, pk):
        data = request.data
        data['user_info'] = self.get_object().id
        serializer = UserInfoRemarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(UserInfoRemarkSerializer(instance).data)

    @detail_route()
    def scores(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        return Response(CourseScoreSerializer(user_course, many=True).data)


class StudentScoreDetailViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """用户成绩邮寄视图"""
    queryset = StudentScoreDetail.objects.all()
    serializer_class = StudentScoreDetailSerializer
    permission_classes = [BaseOperatePermission]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=self.request.query_params.get('user'))
        except:
            raise exceptions.ValidationError('无效的user')
        self.queryset = self.queryset.filter(user=user)
        return super().list(request, *args, **kwargs)


class StatisticsViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [BaseOperatePermission]

    @list_route()
    def students_overview(self, request):
        students_num = self.queryset.filter(user__role='STUDENT').count()
        personal_file_num = self.queryset.filter(first_name__isnull=False,
                                                 last_name__isnull=False,
                                                 phone__isnull=False,
                                                 gender__isnull=False,
                                                 id_number__isnull=False,
                                                 major__isnull=False,
                                                 gpa__isnull=False).count()
        students_applyed = len(set(Order.objects.all().values_list('user_id', flat=True)))
        students_payed = len(set(Order.objects.filter(status='CONFIRMED').values_list('user_id', flat=True)))
        res = {
            'students_num': students_num,
            'personal_file_num': personal_file_num,
            'students_applyed': students_applyed,
            'students_payed': students_payed
        }
        return Response(res)

    @list_route()
    def campus_overview(self, request):
        campus = Campus.objects.all()
        return Response(CampusOverViewSerializer(campus, many=True).data)


class SalesManViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = SalesMan.objects.all()
    serializer_class = SalesManSerializer
    permission_classes = [BaseOperatePermission]


class AdminUserOrderViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """学生成绩视图"""
    queryset = UserCourse.objects.all()
    serializer_class = AdminUserCourseSerializer
    filter_class = UserCourseFilterSet
    permission_classes = [BaseOperatePermission]

    @list_route(['PUT'])
    def add_score(self, request):
        serializer = AddUserCourseScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.queryset.filter(user=data['user'], course=data['course'], order=data['order'])\
            .update(score=data['score'], score_grade=data['score_grade'], reporting_time=datetime.datetime.now())
        instance = self.queryset.filter(user=data['user'], course=data['course'], order=data['order']).first()
        return Response(self.get_serializer(instance).data)

    @list_route(['GET', 'PUT'])
    def confirm_course(self, request):
        if request.method == 'GET':
            user_id = self.request.query_params.get('user')
            try:
                user = User.objects.get(id=user_id)
            except:
                raise exceptions.ValidationError('无效的user')
            user_course = UserCourse.objects.filter(user=user)
            return Response(ConfirmCourseSerializer(user_course, many=True).data)
        else:
            serializer = ConfirmUserCourseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.queryset.filter(user=data['user'], course=data['course'],
                                 project=data['project'], order=data['order']).update(status=data['status'])
            instance = self.queryset.filter(user=data['user'], course=data['course'], order=data['order']).first()
            return Response(self.get_serializer(instance).data)


class AdminUserCourseCreditSwitchViewSet(mixins.ListModelMixin,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         viewsets.GenericViewSet):
    """学生学分转换视图"""
    queryset = UserCourse.objects.filter(user__role='STUDENT')
    serializer_class = AdminCourseCreditSwitchSerializer
    permission_classes = [BaseOperatePermission]

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        try:
            user_id = int(user_id)
        except:
            raise exceptions.ValidationError('请传入正确的user_id')
        return Response(self.serializer_class(self.queryset.filter(user_id=user_id), many=True).data)


class ChildUserViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """子账号管理"""
    queryset = User.objects.exclude(role='STUDENT')
    serializer_class = ChildUserSerializer
    permission_classes = [BaseOperatePermission]

    @detail_route(['PUT'])
    def update_password(self, request, pk):
        instance = self.get_object()
        password = request.data.get('password')
        if not password:
            raise exceptions.ValidationError('请传入正确的password')
        if not len(password) >= 6:
            raise exceptions.ValidationError('密码必须大于6位')
        instance.set_password(password)
        instance.save()
        return Response({'msg': '密码修改成功'})


class AdminCourseViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """管理员选课"""
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [BaseOperatePermission]
    filter_fields = ['user']

    @list_route(['POST'], serializer_class=AdminCreateUserCourseSerializer)
    def create_user_course(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': '选课成功'})

    @list_route()
    def course_to_confirm_count(self, request):
        """用户上传凭证待审核数量"""
        count = UserCourse.objects.filter(status='TO_CONFIRM').count()
        return Response({'course_to_confirm_count': count})


class AdminOrderViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """管理员订单管理"""
    queryset = Order.objects.all().select_related('user').prefetch_related('orderchartrelation_set__chart',
                                                                           'usercourse_set')
    serializer_class = AdminOrderSerializer
    permission_classes = [BaseOperatePermission]
    filter_fields = ['currency', 'payment', 'status', 'user']

    @detail_route(['put'])
    def confirm(self, request, pk):
        """订单支付成功与否确认"""
        instance = self.get_object()
        if request.data.get('status') == 'CONFIRMED':
            status = 'CONFIRMED'
            remark = '订单支付成功，已确认'
        elif request.data.get('status') == 'CONFIRMED_FAILED':
            status = 'CONFIRMED_FAILED'
            remark = '订单支付失败，验证失败'
        else:
            raise exceptions.ValidationError('请传入正确的status参数')
        if instance.status != 'TO_CONFIRM':
            raise exceptions.ValidationError('仅能操作待确认状态下的订单')
        if request.user.role != 'ADMIN':
            raise exceptions.ValidationError('仅管理员有权限确认订单')
        if instance.status != 'TO_CONFIRM':
            raise exceptions.ValidationError('仅能操作待确认下的订单')
        instance.status = status
        instance.save()
        if instance.coupon_list:
            # 如果使用了优惠券，更新优惠券的状态
            coupon_list = json.loads(instance.coupon_list)
            UserCoupon.objects.filter(user=instance.user, coupon__id__in=coupon_list).update(
                status='USED' if status == 'CONFIRMED' else 'TO_USE')
        HistoryFactory.create_record(operator=request.user, source=instance, key='UPDATE', remark=remark,
                                     source_type='ORDER')
        return Response(self.serializer_class(instance).data)


class NavigationViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = FirstLevel.objects.order_by('rank')
    serializer_class = FirstLevelSerializer
    pagination_class = None
    permission_classes = [BaseOperatePermission]

    def get_queryset(self):
        menus = {
            'ADMIN': ['CONSULTATION_CENTER', 'FINANCIAL_CENTER', 'PRODUCT_CENTER', 'MARKET_CENTER', 'SALES_CENTER',
                      'SYSTEM_CENTER'],
            'FINANCE': ['CONSULTATION_CENTER', 'FINANCIAL_CENTER'],
            'PRODUCT': ['PRODUCT_CENTER'],
            'MARKET': ['MARKET_CENTER'],
            'SALES': ['SALES_CENTER']
        }
        queryset = self.queryset.filter(key__in=menus.get(self.request.user.role))
        return queryset