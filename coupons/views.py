# coding: utf-8
from rest_framework import mixins, viewsets
from coupons.models import Coupon
from coupons.serializers import CouponSerializer


class CouponViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer