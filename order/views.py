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
        order = self.queryset.filter(user=self.request.user, status='TO_PAY').last()
        if order:
            return Response(self.get_serializer(order).data)
        return Response({'code': 100, 'msg': '没有未完成的订单，可以创建'})


class OrderPaymentViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     order_instance = Order.objects.get(id=serializer.data['order'])
    #     serializer = OrderSerializer(order_instance, context={'request': request})
    #     return Response(serializer.data)