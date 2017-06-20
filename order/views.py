# coding: utf-8
from rest_framework import mixins, viewsets
from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer