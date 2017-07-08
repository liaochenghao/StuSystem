# coding: utf-8
from rest_framework.routers import SimpleRouter
from admin.views import AccountInfoViewSet, UserInfoViewSet, UserScoreDetailViewSet, ProjectViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)
router.register('user_info', UserInfoViewSet)
router.register('student/score_info', UserScoreDetailViewSet)
router.register('project', ProjectViewSet)

urlpatterns = router.urls