# coding: utf-8
from coupon.serializers import CouponSerializer, UserCouponSerializer
from permissions.base_permissions import CreateCouponOperatePermission, UserCouponOperatePermission
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from coupon.models import Coupon, UserCoupon


class CouponViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [CreateCouponOperatePermission]


class UserCouponViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = UserCoupon.objects.all()
    serializer_class = UserCouponSerializer
    permission_classes = [UserCouponOperatePermission]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': '操作成功'})