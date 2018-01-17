# coding: utf-8
from admin.models import PaymentAccountInfo
from common.models import SalesManUser
from common.serializers import CampusSerializer
from coupon.models import UserCoupon
from source.models import Campus
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from authentication.models import UserInfo
from order.models import Order, UserCourse
from utils.functions import get_key_verbose_data


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