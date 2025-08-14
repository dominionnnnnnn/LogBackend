from django.urls import path
from .views import CreateDepartmentView, CreateSchoolView, SchoolListView, DepartmentListView

urlpatterns = [
    path('register-school/', CreateSchoolView.as_view(), name='school-registration'),
    path('register-department/', CreateDepartmentView.as_view(), name='school-registration'),
    path('list-school/', SchoolListView.as_view(), name='school-registration'),
    path('list-department/', DepartmentListView.as_view(), name='school-registration'),
]
