# coding: utf-8
from market.serializers import ChannelSerializer
from rest_framework import mixins, viewsets

from market.models import Channel
from permissions.base_permissions import BaseOperatePermission


class ChannelViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [BaseOperatePermission]
