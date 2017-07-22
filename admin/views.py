# coding: utf-8
from rest_framework import mixins, viewsets, views
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer, \
    UserInfoRemarkSerializer, ConfirmCourseSerializer, CourseScoreSerializer, UserScoreDetailSerializer, \
    AdminProjectSerializer, CampusOverViewSerializer, SalsesManSerializer, AdminUserCourseSerializer, \
    AdminProjectResultSerializer
from course.models import Project, Campus, ProjectResult
from common.models import SalesMan
from order.models import UserCourse, Order
from authentication.models import UserInfo, UserScoreDetail
from admin.filters import UserInfoFilterSet
from rest_framework import exceptions
from utils.mysql_db import execute_sql


class AccountInfoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = PaymentAccountInfo.objects.all()
    serializer_class = PaymentAccountInfoSerializer


class UserInfoViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilterSet

    def get_queryset(self):
        if self.request.user.role != 'ADMIN':
            raise exceptions.PermissionDenied('非管理员无权限访问该接口')
        queryset = self.queryset.exclude(user__role='ADMIN')
        return queryset

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
    def confirm_course(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        return Response(ConfirmCourseSerializer(user_course, many=True).data)

    @detail_route()
    def scores(self, request, pk):
        user = self.get_object().user
        user_course = UserCourse.objects.filter(user=user)
        return Response(CourseScoreSerializer(user_course, many=True).data)


class UserScoreDetailViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    queryset = UserScoreDetail.objects.all()
    serializer_class = UserScoreDetailSerializer

    def get_object(self):
        # pk 传过来的是user_id，需要转换为user_score_detail
        user_id = self.kwargs.get('pk')
        try:
            user_info = self.queryset.get(user=user_id)
        except UserScoreDetail.DoesNotExist:
            raise exceptions.NotFound('未找到user_info实例')
        return user_info


class AdminProjectViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = AdminProjectSerializer


class StatisticsViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    @list_route()
    def students_overview(self, request):
        students_num = self.queryset.count()
        personal_file_num = self.queryset.filter(first_name__isnull=False,
                                                 last_name__isnull=False,
                                                 phone__isnull=False,
                                                 gender__isnull=False,
                                                 id_number__isnull=False,
                                                 major__isnull=False,
                                                 gpa__isnull=False).count()
        # students_applyed = Order.objects.extra(select={'a': 'GROUP BY user_id'}).count()
        # students_payed = Order.objects.filter(status='CONFIRMED').count()
        students_applyed = len(execute_sql('select * from stu_system.order GROUP by user_id'))
        students_payed = len(execute_sql('select * from stu_system.order where status="CONFIRMED" GROUP by user_id'))
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
    serializer_class = SalsesManSerializer


class AdminUserOrderViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """学生成绩视图"""
    queryset = UserCourse.objects.all()
    serializer_class = AdminUserCourseSerializer


class AdminUserProjectResultViewSet(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    viewsets.GenericViewSet):
    """学生学分转换视图"""
    queryset = ProjectResult.objects.all()
    serializer_class = AdminProjectResultSerializer