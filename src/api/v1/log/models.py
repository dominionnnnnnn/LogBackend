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
    
class Comment(models.Model):
    content = models.CharField(max_length=255)
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='comments')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={"role": "supervisor"}, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # class Meta:
    #     unique_together = ('content', 'log')

    def __str__(self):
        return f"{self.content} ({self.supervisor.email})"