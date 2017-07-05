# coding: utf-8
from rest_framework import mixins, viewsets
from admin.models import PaymentAccountInfo
from admin.serializers import PaymentAccountInfoSerializer


class AccountInfoViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = PaymentAccountInfo.objects.all()
    serializer_class = PaymentAccountInfoSerializer