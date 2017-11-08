# coding: utf-8
from rest_framework.filters import FilterSet

from order import Order


class OrderFilterSet(FilterSet):

    class Meta:
        model = Order
        fields = ['user']