from django.urls import path
from .views import UserRegistrationView, UserProfileSetupView, UserProfilePhotoUpdateView, VerifyCodeView, UserDetailView, AssignSupervisorView, ListStudentView,ListSupervisorView , ResendVerificationCodeView, ListAssignedStudentsView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-code'),
    path('profile/setup/', UserProfileSetupView.as_view(), name='user-profile-setup'),
    path('profile/photo/', UserProfilePhotoUpdateView.as_view(), name='user-profile-photo-update'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('detail/', UserDetailView.as_view(), name='user-detail'),
    path('list-students/', ListStudentView.as_view(), name='list-students'),
    path('list-supervisors/', ListSupervisorView.as_view(), name='list-supervisors'),
    path('list-assigned-students/', ListAssignedStudentsView.as_view(), name='list-assigned-students'),
    path('assign-supervisor/<int:student_id>/', AssignSupervisorView.as_view(), name='assign-supervisor'),
]
