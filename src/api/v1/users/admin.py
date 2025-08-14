from django.contrib import admin
from .models import User, StudentProfile, SupervisorProfile, AdminProfile

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(SupervisorProfile)
admin.site.register(AdminProfile)
