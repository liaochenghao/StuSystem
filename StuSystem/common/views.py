# coding: utf-8
import time

from admin.models import PaymentAccountInfo
from common.models import SalesManUser
from common.serializers import CommonNoticeSerializer
from coupon.models import UserCoupon
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from authentication.models import UserInfo
from order.models import Order, UserCourse
from utils.functions import get_key_verbose_data, handle_mongodb_cursor_data
from utils.mongodb import stu_db


class GlobalEnumsViewSet(APIView):
    def get(self, request):
        res = {
            'account_payment': get_key_verbose_data(dict(PaymentAccountInfo.PAYMENT)),
            'account_currency': get_key_verbose_data(dict(PaymentAccountInfo.CURRENCY)),
            'user_info_gender': get_key_verbose_data(dict(UserInfo.GENDER)),
            'user_grade': get_key_verbose_data(dict(UserInfo.GRADE)),
            'order_payment': get_key_verbose_data(dict(Order.PAYMENT)),
            'order_currency': get_key_verbose_data(dict(Order.CURRENCY)),
            'order_status': get_key_verbose_data(dict(Order.STATUS)),
            'user_status': get_key_verbose_data(dict(SalesManUser.STATUS)),
            'course_credit_switch': get_key_verbose_data(dict(UserCourse.CREDIT_SWITCH_STATUS)),
            'user_course_status': get_key_verbose_data(dict(UserCourse.STATUS)),
            'coupon_status': get_key_verbose_data(dict(UserCoupon.STATUS)),
            'user_role': get_key_verbose_data(dict(User.ROLE)),
        }
        return Response(res)


class CommonNoticeViewSet(APIView):
    def get(self, request):
        notice_message = handle_mongodb_cursor_data(
            stu_db.find(
                collection_name='message_auto_notice',
                pagination=True,
                sort_field=("_id", -1),
                search_data={
                    'user_id': request.user.id,
                    'read': {'$ne': True},
                }
            )
        )
        return Response(notice_message)

    def put(self, request):
        serializer = CommonNoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        stu_db.update_many(collection_name='message_auto_notice',
                           search_data={'user_id': request.user.id, 'module_name': validated_data['module_name']},
                           update_data={"$set": {'read': True}})
        return Response({'msg': '操作成功'})


class OrderCurrencyPaymentViewSet(APIView):
    def get(self, request):
        payment = PaymentAccountInfo.objects.all()
        inland_bank = payment.filter(payment='BANK', currency='RMB'). \
            values('payment', 'currency', 'account_number', 'account_name', 'opening_bank', )
        international_bank = payment.filter(payment='BANK', currency='FOREIGN_CURRENCY'). \
            values('payment', 'currency', 'account_number', 'account_name', 'pay_link')
        ali_pay = payment.filter(payment='ALI_PAY'). \
            values('payment', 'currency', 'account_number', 'account_name', )
        pay_pal = payment.filter(payment='PAY_PAL'). \
            values('payment', 'opening_bank', 'currency', 'account_name', 'swift_code', 'routing_number_paper',
                   'swift_code_foreign_currency', 'company_address', 'account_number', 'routing_number_wires')
        res = [
            {
                'key': 'FOREIGN_CURRENCY',
                'verbose': dict(PaymentAccountInfo.CURRENCY).get('FOREIGN_CURRENCY'),
                'payment': [
                    {
                        'key': 'BANK',
                        'verbose': dict(PaymentAccountInfo.PAYMENT).get('BANK'),
                        'payment_information': international_bank
                    },
                    {
                        'key': 'PAY_PAL',
                        'verbose': dict(PaymentAccountInfo.PAYMENT).get('PAY_PAL'),
                        'payment_information': pay_pal
                    }
                ]
            },
            {
                'key': 'RMB',
                'verbose': dict(PaymentAccountInfo.CURRENCY).get('RMB'),
                'payment': [
                    {
                        'key': 'BANK',
                        'verbose': dict(PaymentAccountInfo.PAYMENT).get('BANK'),
                        'payment_information': inland_bank
                    },
                    {
                        'key': 'ALI_PAY',
                        'verbose': dict(PaymentAccountInfo.PAYMENT).get('ALI_PAY'),
                        'payment_information': ali_pay
                    },
                ]
            }
        ]
        return Response(res)