# tasks/models.py
# tasks/models.py

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Manually set a default value here

    def __str__(self):
        return self.title

