from django.urls import path
from .views import LogCreateView, LogListView, LogUpdateStatusView , CommentCreateView, CommentListView, LogUpdateView, LogDeleteView

urlpatterns = [
    path('create/', LogCreateView.as_view(), name='log-create'),
    path('update/<int:pk>/', LogUpdateView.as_view(), name='log-update'),
    path('delete/<int:pk>/', LogDeleteView.as_view(), name='log-delete'),
    path('list/', LogListView.as_view(), name='log-list'),
    path('<int:pk>/status/', LogUpdateStatusView.as_view(), name='log-update-status'),
    path('<int:log_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('comment/', CommentCreateView.as_view(), name='comment-create'),
]
    