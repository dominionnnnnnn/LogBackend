from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import random
from django.utils import timezone
from datetime import timedelta
from api.v1.school.models import School, Department

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role'] 
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_verification_code(self):
        code = f"{random.randint(100000, 999999)}"
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=3)
        self.save()
        return code
    
    objects = CustomUserManager()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    photo = models.ImageField(upload_to='profile_photos/students/', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    matric_number = models.CharField(max_length=50, unique=True)
    organisation_name = models.CharField(max_length=100, null=True)
    internship_location = models.CharField(max_length=100, null=True)
    internship_start = models.DateField()
    internship_end = models.DateField()
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_students',
        limit_choices_to={'role': 'supervisor'}
    )
    
    def __str__(self):
        return self.user.full_name

class SupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')
    photo = models.ImageField(upload_to='profile_photos/supervisors/', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    office = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return self.user.full_name
    
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    photo = models.ImageField(upload_to='profile_photos/admins/', blank=True, null=True)
    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin')
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return self.user.full_name