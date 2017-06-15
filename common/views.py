# coding: utf-8
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campus
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
            'user_info_gender': get_key_verbose_data(dict(UserInfo.GENDER))
        }
        return Response(res)