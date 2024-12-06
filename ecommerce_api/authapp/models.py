from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=225)
    age = models.PositiveIntegerField()  
    email = models.EmailField(max_length=255, unique=True)  
    ph_num = models.CharField(max_length=15, unique=True) 
    password = models.CharField(max_length=255)
    username = None
    is_admin = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email  
