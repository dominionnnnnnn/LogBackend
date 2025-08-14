from django.urls import path
from .views import UserRegistrationView, UserProfileSetupView, UserProfilePhotoUpdateView, VerifyCodeView, UserDetailView, AssignSupervisorView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profile/setup/', UserProfileSetupView.as_view(), name='user-profile-setup'),
    path('profile/photo/', UserProfilePhotoUpdateView.as_view(), name='user-profile-photo-update'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('detail/', UserDetailView.as_view(), name='user-detail'),
    path('assign-supervisor/<int:student_id>/', AssignSupervisorView.as_view(), name='assign-supervisor'),
]
