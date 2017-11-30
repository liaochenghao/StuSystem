# coding: utf-8
from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from .views import GlobalEnumsViewSet

router = SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    url(r'^global_enums', GlobalEnumsViewSet.as_view())
]