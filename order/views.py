# coding: utf-8
from rest_framework import mixins, viewsets
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

    def create(self, request, *args, **kwargs):
        order = self.queryset.filter(user=self.request.user).exclude(status='CONFIRMED').last()
        if order:
            return Response(self.get_serializer(order).data)
        return super().create(request, args, kwargs)


class OrderPaymentViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer