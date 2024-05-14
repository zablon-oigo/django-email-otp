from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager
import secrets
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(verbose_name="Email address", unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateTimeField(default=timezone.now)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()

    def __str__(self):
        return self.email

class OTPToken(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp_code=models.CharField(max_length=6,default=secrets.token_hex(3))
    created=models.DateTimeField(auto_now_add=True)
    expire=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email