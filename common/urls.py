# coding: utf-8
from rest_framework.routers import SimpleRouter
from .views import CampusViewSet

router = SimpleRouter()

router.register('campus', CampusViewSet)
urlpatterns = router.urls