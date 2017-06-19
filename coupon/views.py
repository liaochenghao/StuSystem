# coding: utf-8
from rest_framework import mixins, viewsets
from .models import Coupon, UserCoupon
from .serializers import CouponSerializer, UserCouponSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @detail_route(methods=['post'])
    def add_coupon(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.create_coupon()
        response = Response(res)
        return response
    def 


class UserCouponViewSet(viewsets.ModelViewSet):
    queryset = UserCoupon.objects.all()
    serializer_class = UserCouponSerializer