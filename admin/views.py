# coding: utf-8
from rest_framework import mixins, viewsets
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer, UserInfoSerializer
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

    def list(self, request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            raise exceptions.PermissionDenied('非管理员无权限访问该接口')
        self.queryset = self.queryset.exclude(user__role='ADMIN')
        return super().list(request, *args, **kwargs)