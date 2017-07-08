# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer, \
    UserInfoRemarkSerializer, ConfirmCourseSerializer, CourseScoreSerializer, UserScoreDetailSerializer, AdminProjectSerializer
from course.models import UserCourse, Project
from authentication.models import UserInfo, UserScoreDetail
from admin.filters import UserInfoFilterSet
from rest_framework import exceptions


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