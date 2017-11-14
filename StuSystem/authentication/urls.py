# coding: utf-8
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserInfoViewSet, StudentScoreDetailViewSet

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('user/info', UserInfoViewSet)
router.register('user/score_detail', StudentScoreDetailViewSet)

urlpatterns = router.urls