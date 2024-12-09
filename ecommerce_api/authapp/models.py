from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=225)
    age = models.PositiveIntegerField(null=False, blank=False, default=18)  
    email = models.EmailField(max_length=255, unique=True)  
    ph_num = models.CharField(max_length=15, unique=True) 
    photo =  models.ImageField(upload_to ='profile_photos/', null=True, blank=True) 
    username = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email  

class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="otp")
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
        
    def is_valid(self):
        expiration_duration = timedelta(minutes=5)
        return now() < self.created_at + expiration_duration
    
    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp_code}"