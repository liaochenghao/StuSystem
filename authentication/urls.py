# coding: utf-8
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserInfoViewSet, UserScoreDetailViewSet

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('user/info', UserInfoViewSet)
router.register('user/score_detail', UserScoreDetailViewSet)

urlpatterns = router.urls