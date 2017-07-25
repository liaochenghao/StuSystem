# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from course.models import Campus, ProjectResult
from order.models import Order, UserCourse
from authentication.models import UserInfo
from admin.models import PaymentAccountInfo
from common.models import SalesManUser
from coupon.models import UserCoupon
from common.serializers import CampusSerializer
from utils.functions import get_key_verbose_data


class CampusViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class GlobalEnumsViewSet(APIView):
    def get(self, request):
        res = {
            'account_payment': get_key_verbose_data(dict(PaymentAccountInfo.PAYMENT)),
            'user_info_gender': get_key_verbose_data(dict(UserInfo.GENDER)),
            'order_payment': get_key_verbose_data(dict(Order.PAYMENT)),
            'order_currency': get_key_verbose_data(dict(Order.CURRENCY)),
            'order_status': get_key_verbose_data(dict(Order.STATUS)),
            'user_status': get_key_verbose_data(dict(SalesManUser.STATUS)),
            'project_result': get_key_verbose_data(dict(ProjectResult.STATUS)),
            'user_course_status': get_key_verbose_data(dict(UserCourse.STATUS)),
            'coupon_status': get_key_verbose_data(dict(UserCoupon.STATUS))
        }
        return Response(res)