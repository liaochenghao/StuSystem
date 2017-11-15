# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from authentication.models import User
from order.models import Order, OrderPayment, UserCourse, ShoppingChart
from order.serializers import OrderSerializer, OrderPaymentSerializer, UserOrderCourseSerializer, ShoppingChartSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    filter_fields = ['currency', 'payment', 'status', 'user']

    def get_serializer(self, *args, **kwargs):
        try:
            user = User.objects.get(id=int(self.request.query_params.get('user')))  # 如果管理后台传入了user，则获取该user
        except Exception as e:
            user = self.request.user
        self.request.user = user
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('none_canceled_order'):
            queryset = queryset.exclude(status='CANCELED')
        return queryset

    @list_route()
    def check_order(self, request):
        order = self.queryset.filter(user=self.request.user, status__in=['TO_PAY', 'TO_CONFIRM', 'CONFIRMED']).first()
        if order:
            order_course_count = UserCourse.objects.filter(order=order).count()
            if order_course_count < int(order.course_num):
                return Response(self.get_serializer(order).data)
        return Response({'code': 100, 'msg': '没有未完成的订单，可以创建'})

    @list_route()
    def order_currency_payment(self, request):
        """订单币种及支付方式"""
        data = [
            {
                'key': 'DOLLAR',
                'verbose': dict(Order.CURRENCY).get('DOLLAR'),
                'payment': [
                    {
                        'key': 'BANK',
                        'verbose': dict(Order.PAYMENT).get('BANK')
                    },
                    {
                        'key': 'PAY_PAL',
                        'verbose': dict(Order.PAYMENT).get('PAY_PAL')
                    }
                ]
            },
            {
                'key': 'RMB',
                'verbose': dict(Order.CURRENCY).get('RMB'),
                'payment': [
                    {
                        'key': 'BANK',
                        'verbose': dict(Order.PAYMENT).get('BANK')
                    },
                    {
                        'key': 'ALI_PAY',
                        'verbose': dict(Order.PAYMENT).get('ALI_PAY')
                    },
                    {
                        'key': 'OFF_LINE',
                        'verbose': dict(Order.PAYMENT).get('OFF_LINE')
                    }
                ]
            }
        ]
        return Response(data)

    @list_route()
    def user_order_list(self, request):
        user = request.user
        status = self.request.query_params.get('status')
        none_canceled_order = self.request.query_params.get('none_canceled_order')
        user_orders = self.queryset.filter(user=user).exclude()
        if status:
            user_orders = user_orders.filter(status=status)
        if none_canceled_order:
            user_orders = user_orders.exclude(status='CANCELED')
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


class ShoppingChartViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = ShoppingChart.objects.filter(status='NEW')
    serializer_class = ShoppingChartSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_destroy(self, instance):
        instance.status = 'DELETED'
        instance.save()