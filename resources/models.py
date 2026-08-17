from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ResourceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Resource(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='resources')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=500,blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
