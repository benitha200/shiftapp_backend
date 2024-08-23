# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('shift_leader', 'shift_leader'),
        ('manager', 'Manager')
    ])
    # Add other custom fields as needed
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email