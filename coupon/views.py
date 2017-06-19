# coding: utf-8
from rest_framework import mixins, viewsets
from coupon.models import Coupon, UserCoupon
from coupon.serializers import CouponSerializer, UserCouponSerializer


class CouponViewSet(mixins.CreateModelMixin,
                    viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class UserCouponViewSet(viewsets.ModelViewSet):
    queryset = UserCoupon.objects.all()
    serializer_class = UserCouponSerializer