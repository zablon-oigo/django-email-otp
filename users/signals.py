from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from .models import OTPToken
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            OTPToken.objects.create(user=instance, expire=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active = False
            instance.save()

            otp = OTPToken.objects.filter(user=instance).last()
            subject = "Email Verification"
            message = f"""
                        Hello {instance.email}, here is your OTP {otp.otp_code}
                        It expires in 5 minutes. Use the URL below to redirect back to the website:
                        http://127.0.0.1:8000/verify-email/{instance.email}
                    """
            sender = settings.DEFAULT_FROM_EMAIL
            receiver = [instance.email, ]
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
