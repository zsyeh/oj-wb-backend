# leave/urls.py

from django.urls import include, path
from .views import request_leave, approve_leave
from .views import RegisterView
from .views import AdminLeaveListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import cancel_leave
from .views import UserInfoView
from .views import reject_leave
from .views import complete_leaving
from .views import get_student_leaves,ChangePasswordView,pre_approve_leave,mas_approve_leave
urlpatterns = [
    path('request-leave/', request_leave, name='request_leave'),#请假
    path('view-leave/', get_student_leaves, name='view_leave_status'),#查看请假状态
    path('admin/approve-leave/<int:leave_id>/', approve_leave, name='approve_leave'),#批准请假
    path('register/', RegisterView.as_view(), name='register'),#注册
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#登录（内置函数）
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/leaves/', AdminLeaveListView, name='admin_leave_list'),
    path('admin/leaves/approve/<int:leave_id>/', AdminLeaveListView, name='approve_leave'),
    path('cancel-leave/<int:leave_id>/', cancel_leave, name='cancel_leave'),#取消请假
    path('UserInfoView/', UserInfoView, name='UserInfoView'),#查看用户信息
    path('admin/reject-leave/<int:leave_id>/', reject_leave, name='rejected_leave'),#拒绝请假
    path('CompleteLeavingView/<int:leave_id>/', complete_leaving, name='CompleteLeavingView'),#完成请假(销假)
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('pre_approve_leave/<int:leave_id>/', pre_approve_leave, name='pre_approve_leave'),
    path('mas_approve_leave/<int:leave_id>/', mas_approve_leave, name='mas_approve_leave'),
]

