from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import EmailVerification
from django.urls import reverse, NoReverseMatch
import logging
from config.config import BASE_BACK_URL
from .utils import trigger_verification_email 


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        success, message = trigger_verification_email(instance)
        if not success:
            # Already logged inside the function
            pass