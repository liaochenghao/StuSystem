# coding: utf-8
from rest_framework.routers import DefaultRouter
from coupon import views

router = DefaultRouter()
router.register('coupon', UserViewSet)

urlpatterns = router.urls