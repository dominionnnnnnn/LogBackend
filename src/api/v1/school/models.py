from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    website = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='profile_photos/school/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    
    class Meta:
        unique_together = ('name', 'school')

    def __str__(self):
        return f"{self.name} ({self.school.name})"
