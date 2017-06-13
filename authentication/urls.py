# coding: utf-8
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserInfoViewSet

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('user/info', UserInfoViewSet)

urlpatterns = router.urls