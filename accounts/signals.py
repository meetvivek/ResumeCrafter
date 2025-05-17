from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import EmailVerification
from django.urls import reverse, NoReverseMatch
import logging
from config.config import BASE_BACK_URL
from .utils import send_verification_email_html 


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        try:
            # Create email verification token
            email_verif, _ = EmailVerification.objects.get_or_create(user=instance)

            # Build the verification link
            try:
                path = reverse("email-verify", kwargs={"token": str(email_verif.token)})
            except NoReverseMatch as e:
                logger.error(f"URL reverse error: {e}")
                return

            verification_url = f"{BASE_BACK_URL}{path}"

            try:
                send_verification_email_html(instance, verification_url)
                logger.info(f"[Email Verification] Email successfully sent to {instance.email}")
            except Exception as e:
                logger.exception(f"[Email Verification] Failed to send email to {instance.email}: {e}")
                
            # # Compose and send email
            # subject = "Verify your email for ResumeCrafter"
            # message = f"Hi {instance.first_name},\n\nPlease verify your email by clicking the link below:\n{verification_url}\n\nThank you!"

            # sent_staus =  send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])
            # if sent_staus:
            #     logger.info(f"[Email Verification] Email successfully sent to {instance.email}")
            # else:
            #     logger.warning(f"[Email Verification] Email sending failed silently to {instance.email}")

        except Exception as e:
            logger.exception(f"Failed to send verification email: {e}")
