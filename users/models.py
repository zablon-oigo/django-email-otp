from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(verbose_name="Email address", unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateTimeField(default=timezone.now)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    