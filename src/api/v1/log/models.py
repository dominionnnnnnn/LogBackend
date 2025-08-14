from django.db import models
from django.conf import settings

# Create your models here.
class Log(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.status}"