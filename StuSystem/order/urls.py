# coding: utf-8
from rest_framework.routers import SimpleRouter

from order.views import OrderViewSet, OrderPaymentViewSet, ShoppingChartViewSet

router = SimpleRouter()
router.register('order_payment', OrderPaymentViewSet)
router.register('shopping_chart', ShoppingChartViewSet)
router.register('', OrderViewSet)
urlpatterns = router.urls