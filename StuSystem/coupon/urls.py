# coding: utf-8
from rest_framework.routers import SimpleRouter

from coupon.views import CouponViewSet, UserCouponViewSet

router = SimpleRouter()
router.register('coupon', CouponViewSet)
router.register('user_coupon', UserCouponViewSet)

urlpatterns = router.urls