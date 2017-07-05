# coding: utf-8
from rest_framework.routers import SimpleRouter
from admin.views import AccountInfoViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)

urlpatterns = router.urls