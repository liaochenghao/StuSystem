# coding: utf-8
from rest_framework.routers import SimpleRouter
from coupons.views import CouponViewSet

router = SimpleRouter()
router.register('coupon', CouponViewSet)

urlpatterns = router.urls