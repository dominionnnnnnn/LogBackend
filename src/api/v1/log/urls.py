from django.urls import path
from .views import LogCreateView, LogListView, LogUpdateStatusView

urlpatterns = [
    path('create/', LogCreateView.as_view(), name='log-create'),
    path('list/', LogListView.as_view(), name='log-list'),
    path('<int:pk>/status/', LogUpdateStatusView.as_view(), name='log-update-status'),
]
    