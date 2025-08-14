from django.urls import path, include

urlpatterns = [
   path('users/', include('api.v1.users.urls')),
   path('log/', include('api.v1.log.urls')),
   path('school/', include('api.v1.school.urls')),
]
