# coding: utf-8
from rest_framework.routers import SimpleRouter

from admin.views import AccountInfoViewSet, UserInfoViewSet, StudentScoreDetailViewSet, \
    StatisticsViewSet, SalesManViewSet, AdminUserOrderViewSet, AdminUserCourseCreditSwitchViewSet, ChildUserViewSet, \
    AdminCourseViewSet, AdminOrderViewSet

router = SimpleRouter()

router.register('account_info', AccountInfoViewSet)
router.register('user_info', UserInfoViewSet)
router.register('student/score_info', StudentScoreDetailViewSet)
router.register('statistics', StatisticsViewSet)
router.register('sales_man', SalesManViewSet)
router.register('user_course', AdminUserOrderViewSet)
router.register('course_credit_switch', AdminUserCourseCreditSwitchViewSet)
router.register('child_user', ChildUserViewSet)
router.register('course', AdminCourseViewSet)
router.register('order', AdminOrderViewSet)

urlpatterns = router.urls