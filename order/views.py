# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import list_route
from order.models import Order, OrderPayment
from order.serializers import OrderSerializer, OrderPaymentSerializer
from rest_framework.response import Response


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @list_route()
    def check_order(self, request):
        order = self.queryset.filter(user=self.request.user).exclude(status='CONFIRMED').last()
        if order:
            return Response(self.get_serializer(order).data)
        return Response({'code': ''})


class OrderPaymentViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer