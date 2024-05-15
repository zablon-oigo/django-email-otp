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

        else:
            OTPToken.objects.create(user=instance, expire=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active=False 
            instance.save()

        otp = OTPToken.objects.filter(user=instance).last()
        subject="Email Verification"
        message = f"""
                        Hello {instance.email}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{instance.email}
                                
                                """