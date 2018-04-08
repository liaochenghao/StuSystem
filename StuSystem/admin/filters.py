# coding: utf-8
import django_filters
from rest_framework.filters import FilterSet

from authentication.models import UserInfo
from order.models import UserCourse


class UserInfoFilterSet(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    wechat = django_filters.CharFilter(lookup_expr='icontains')
    sales_man = django_filters.CharFilter(lookup_expr='icontains')
    student_status = django_filters.CharFilter(lookup_expr='icontains')
    create_year = django_filters.NumberFilter(name='create_time', lookup_expr='year')

    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'wechat', 'sales_man', 'student_status', 'create_year']


class UserCourseFilterSet(FilterSet):
    class Meta:
        model = UserCourse
        fields = ['user']
