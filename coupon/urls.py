# coding: utf-8
from rest_framework.routers import DefaultRouter
from coupon.views import CouponViewSet

router = DefaultRouter()
router.register('coupon', CouponViewSet)

urlpatterns = router.urls