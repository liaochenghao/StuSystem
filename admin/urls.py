# coding: utf-8
from rest_framework.routers import SimpleRouter
from admin.views import AccountInfoViewSet, UserInfoViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)
router.register('user_info', UserInfoViewSet)

urlpatterns = router.urls