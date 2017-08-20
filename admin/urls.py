# coding: utf-8
from rest_framework.routers import SimpleRouter
from admin.views import AccountInfoViewSet, UserInfoViewSet, UserScoreDetailViewSet, AdminProjectViewSet, \
    StatisticsViewSet, SalesManViewSet, AdminUserOrderViewSet, AdminUserProjectResultViewSet, ChildUserViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)
router.register('user_info', UserInfoViewSet)
router.register('student/score_info', UserScoreDetailViewSet)
router.register('project', AdminProjectViewSet)
router.register('statistics', StatisticsViewSet)
router.register('sales_man', SalesManViewSet)
router.register('user_course', AdminUserOrderViewSet)
router.register('project_result', AdminUserProjectResultViewSet)
router.register('child_user', ChildUserViewSet)

urlpatterns = router.urls