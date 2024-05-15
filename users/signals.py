from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTPToken
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()

@receiver(post_save, sender=User) 
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass