# coding: utf-8
import json

from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from authentication.models import User
from coupon.models import UserCoupon
from operate_history.models import OrderOperateHistory
from order.models import Order, OrderPayment, UserCourse, ShoppingChart
from order.serializers import OrderSerializer, OrderPaymentSerializer, UserOrderCourseSerializer, \
    ShoppingChartSerializer, SimpleUserOrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all().order_by('-id').prefetch_related('orderchartrelation_set',
                                                                    'orderchartrelation_set__chart')
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
    def last_order(self, request):
        instance = self.queryset.filter(user=request.user).exclude(status='CANCELED').first()
        if instance:
            data = self.serializer_class(instance).data
            order_chart_relations = instance.orderchartrelation_set.all()
            courses_to_select_count = sum([order_chart.chart.course_num for order_chart in order_chart_relations])
            course_current_selected_count = instance.usercourse_set.all().count()
            data['course_to_select'] = True if instance.status == 'CONFIRMED' \
                                           and courses_to_select_count != course_current_selected_count else False
        else:
            data = {
                "course_to_select": False
            }
        return Response(data)

    @list_route()
    def check_order(self, request):
        if self.queryset.filter(user=self.request.user, status__in=['TO_PAY', 'TO_CONFIRM']).exists():
            order_to = self.get_queryset().filter(user=self.request.user, status__in=['TO_PAY', 'TO_CONFIRM']).first()
            return Response(self.serializer_class(order_to).data)
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

    @detail_route(['put'])
    def cancel(self, request, pk):
        """取消订单"""
        instance = self.get_object()
        if instance.status == 'CANCELED':
            raise exceptions.ValidationError('订单已被取消')
        elif instance.status != 'TO_PAY':
            raise exceptions.ValidationError('无法取消该订单')
        instance.status = 'CANCELED'
        instance.save()
        if instance.coupon_list:
            # 如果使用了优惠券，将优惠券置为可用状态
            coupon_list = json.loads(instance.coupon_list)
            UserCoupon.objects.filter(user=request.user, coupon__id__in=coupon_list).update(status='TO_USE')
        OrderOperateHistory.objects.create(**{'operator': request.user, 'key': 'UPDATE', 'source': instance,
                                              'remark': '取消了订单'})
        return Response(self.serializer_class(instance).data)

    @list_route()
    def user_order_list(self, request):
        """用户订单列表"""
        # todo 暂时不实现下拉翻页功能，待时机成熟再实现
        user = request.user
        status = self.request.query_params.get('status')
        none_canceled_order = self.request.query_params.get('none_canceled_order', True)
        user_orders = self.queryset.filter(user=user).exclude(status='CANCELED')
        if status:
            user_orders = user_orders.filter(status=status)
        if none_canceled_order:
            user_orders = user_orders.exclude(status='CANCELED')
        return Response(SimpleUserOrderSerializer(user_orders, many=True, context={'request': request}).data)

    @list_route()
    def user_order_course(self, request):
        self.serializer_class = UserOrderCourseSerializer
        user = request.user
        user_orders = self.queryset.filter(user=user)
        return Response(self.serializer_class(user_orders, many=True, context={'request': request}).data)


class OrderPaymentViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
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