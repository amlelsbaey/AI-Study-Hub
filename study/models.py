from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='tasks')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class NoteCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notes')

    category = models.ForeignKey(NoteCategory,on_delete=models.CASCADE,related_name='notes')

    courses = models.ManyToManyField(Course,related_name='notes',blank=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class StudySession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='study_sessions')

    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.PositiveIntegerField(
        help_text='Duration in minutes'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title