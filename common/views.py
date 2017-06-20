# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from course.models import Campus
from order.models import Order
from authentication.models import UserInfo
from .serializers import CampusSerializer
from utils.functions import get_key_verbose_data


class CampusViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class GlobalEnumsViewSet(APIView):
    def get(self, request):
        res = {
            'user_info_gender': get_key_verbose_data(dict(UserInfo.GENDER)),
            'order_payment': get_key_verbose_data(dict(Order.PAYMENT)),
            'order_currency': get_key_verbose_data(dict(Order.CURRENCY)),
            'order_status': get_key_verbose_data(dict(Order.STATUS))
        }
        return Response(res)