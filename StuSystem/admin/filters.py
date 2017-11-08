# coding: utf-8
import django_filters
from rest_framework.filters import FilterSet

from authentication.models import UserInfo
from order.models import UserCourse


class UserInfoFilterSet(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    wechat = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'wechat']


class UserCourseFilterSet(FilterSet):

    class Meta:
        model = UserCourse
        fields = ['user']