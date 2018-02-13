# coding: utf-8
from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from .views import GlobalEnumsViewSet, CommonNoticeViewSet, OrderCurrencyPaymentViewSet

router = SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    url(r'^global_enums', GlobalEnumsViewSet.as_view()),
    url(r'^auto_notice', CommonNoticeViewSet.as_view()),
    url(r'^order_currency_payment', OrderCurrencyPaymentViewSet.as_view()),
]
