# coding: utf-8
from rest_framework.routers import SimpleRouter
from order.views import OrderViewSet

router = SimpleRouter()

router.register('', OrderViewSet)
urlpatterns = router.urls