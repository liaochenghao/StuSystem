# coding: utf-8
from rest_framework.filters import FilterSet
from authentication.models import UserInfo
import django_filters


class UserInfoFilterSet(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    wechat = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'wechat']