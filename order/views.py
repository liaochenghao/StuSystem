# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import list_route
from order.models import Order, OrderPayment, UserCourse
from order.serializers import OrderSerializer, OrderPaymentSerializer, UserOrderCourseSerializer
from rest_framework.response import Response


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_fields = ['currency', 'payment', 'status', 'user']

    @list_route()
    def check_order(self, request):
        order = self.queryset.filter(user=self.request.user, status__in=['TO_PAY', 'TO_CONFIRM', 'CONFIRMED']).last()
        if order:
            order_course_count = UserCourse.objects.filter(order=order).count()
            if order_course_count < int(order.course_num):
                return Response(self.get_serializer(order).data)
        return Response({'code': 100, 'msg': '没有未完成的订单，可以创建'})

    @list_route()
    def user_order_list(self, request):
        user = request.user
        user_orders = self.queryset.filter(user=user)
        return Response(self.serializer_class(user_orders, many=True, context={'request': request}).data)

    @list_route()
    def user_order_course(self, request):
        self.serializer_class = UserOrderCourseSerializer
        user = request.user
        user_orders = self.queryset.filter(user=user)
        return Response(self.serializer_class(user_orders, many=True, context={'request': request}).data)


class OrderPaymentViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer