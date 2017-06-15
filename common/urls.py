# coding: utf-8
from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from .views import CampusViewSet, GlobalEnumsViewSet

router = SimpleRouter()

router.register('campus', CampusViewSet)
urlpatterns = router.urls

urlpatterns += [
    url(r'^global_enums', GlobalEnumsViewSet.as_view())
]