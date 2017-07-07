# coding: utf-8
from rest_framework import mixins, viewsets
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer, UserInfoSerializer, RetrieveUserInfoSerializer
from authentication.models import UserInfo
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
            user_info = self.queryset.get(pk=user_id)
        except UserInfo.DoesNotExist:
            raise exceptions.NotFound('未找到user_info实例')
        return user_info