# coding: utf-8
from rest_framework.routers import SimpleRouter

from market.views import ChannelViewSet

router = SimpleRouter()

router.register('channel', ChannelViewSet)

urlpatterns = router.urls