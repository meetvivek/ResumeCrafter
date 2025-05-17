from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_verification_email_html(user, verification_url):
    subject = "Verify your email for ResumeCrafter"
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email

    # Plain text fallback message
    text_content = f"""
    EMAIL VERIFICATION

    Dear {user.first_name},
    Thank you for signing up! To complete your registration, please click the link below to verify your email address:

    {verification_url}

    If you didn't request this verification, please ignore this email.

    Thank you!

    This is an auto-generated email. Please do not reply. 
    @ 2025 ResumeCrafter. All rights reserved.
    """

    try:
        # Render HTML email from a template
        html_content = render_to_string("verification_email.html", {
            "first_name": user.first_name,
            "verification_url": verification_url,
        })

        # Create email message with both plain text and HTML content
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        sent_status = email.send()
        if sent_status:
            logger.info(f"[Email Verification] Email successfully sent to {to_email}")
        else:
            logger.warning(f"[Email Verification] Email sending failed silently to {to_email}")

        logger.info(f"[Email Verification] HTML email successfully sent to {to_email}")
    except Exception as e:
        logger.exception(f"[Email Verification] Failed to send email to {to_email}: {e}")
