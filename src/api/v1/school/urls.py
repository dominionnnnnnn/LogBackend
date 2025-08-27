from django.urls import path
from .views import CreateDepartmentView, CreateSchoolView, SchoolListView, DepartmentListView, SchoolLogoUploadView

urlpatterns = [
    path('register-school/', CreateSchoolView.as_view(), name='school-registration'),
    path('upload-school-logo/', SchoolLogoUploadView.as_view(), name='upload-school-logo'),
    path('register-department/', CreateDepartmentView.as_view(), name='school-registration'),
    path('list-school/', SchoolListView.as_view(), name='school-registration'),
    path('<int:school_id>/departments/', DepartmentListView.as_view(), name='school-registration'),
]
