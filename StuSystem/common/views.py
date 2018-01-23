# coding: utf-8
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
from utils import stu_system


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
        notice_message = handle_mongodb_cursor_data(stu_system.message_auto_notice.find({'user_id': request.user.id,
                                                                                         'read': {'$ne': True}}))
        return Response(notice_message)

    def put(self, request):
        serializer = CommonNoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        stu_system.message_auto_notice.update({'user_id': request.user.id, 'module_name': validated_data['module_name']})
        return Response()