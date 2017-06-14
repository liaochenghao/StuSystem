# coding: utf-8
from rest_framework import mixins, viewsets
from .models import Campus
from .serializers import CampusSerializer


class CampusViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer