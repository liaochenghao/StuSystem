# coding: utf-8
from market.models import Channel
from rest_framework import mixins, viewsets
from market.serializers import ChannelSerializer


class ChannelViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer