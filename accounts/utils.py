from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from config.config import BASE_BACK_URL
import logging
import dns.resolver
import requests
from functools import lru_cache

logger = logging.getLogger(__name__)


def trigger_verification_email(user):
    from accounts.models import EmailVerification

    try:
        email_verif, _ = EmailVerification.objects.get_or_create(user=user)

        try:
            path = reverse("email-verify", kwargs={"token": str(email_verif.token)})
        except NoReverseMatch as e:
            logger.error(f"[Email Verification] URL reverse failed: {e}")
            return False, "Invalid token or URL pattern."

        verification_url = f"{BASE_BACK_URL}{path}"

        try:
            send_verification_email_html(user, verification_url)
            logger.info(f"[Email Verification] Email successfully sent to {user.email}")
            return True, "Verification email sent successfully."
        except Exception as e:
            logger.exception(f"[Email Verification] Failed to send email to {user.email}: {e}")
            return False, "Failed to send verification email."

    except Exception as e:
        logger.exception(f"[Email Verification] Unexpected error: {e}")
        return False, "Something went wrong."

    


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




# URL to a maintained list of disposable email domains
DISPOSABLE_EMAIL_LIST_URL = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/d5e20b926d8dcad50f1a25b832641a4b6fdfbe4f/disposable_email_blocklist.conf"


# Set of known trusted email providers (based on MX records)
TRUSTED_MX_PROVIDERS = {
    "google.com": "Google",
    "zoho.com": "Zoho",
    "outlook.com": "Microsoft",
    "hotmail.com": "Microsoft",
    "yahoo.com": "Yahoo",
    "icloud.com": "Apple",
    "protonmail.ch": "ProtonMail",
    "fastmail.com": "Fastmail",
}


@lru_cache(maxsize=1)
def get_disposable_domains():
    """Fetch and cache the set of known disposable email domains."""
    try:
        response = requests.get(DISPOSABLE_EMAIL_LIST_URL)
        response.raise_for_status()
        domains = set(line.strip().lower() for line in response.text.splitlines() if line.strip())
        return domains
    except Exception as e:
        print("Error fetching disposable domain list:", e)
        return set()


def is_disposable_email(email: str) -> bool:
    domain = email.split('@')[-1].lower()
    return domain in get_disposable_domains()


def get_mail_service_from_mx(email: str) -> str:
    """
    Returns the name of a known email provider based on MX record.
    Returns 'Unknown' if no trusted provider is found.
    """
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        for mx in mx_records:
            mx_host = str(mx.exchange).lower().strip('.')
            for trusted_domain, provider in TRUSTED_MX_PROVIDERS.items():
                if trusted_domain in mx_host:
                    return provider
        return "Unknown"
    except Exception:
        return "Unknown"


def validate_email_address(email: str) -> tuple[bool, str]:
    """
    Final validation function.
    Returns (True, reason) if email is valid.
    Returns (False, reason) if email is disposable or from an unknown provider.
    """
    if is_disposable_email(email):
        return False, "Disposable email addresses are not allowed."

    provider = get_mail_service_from_mx(email)
    if provider == "Unknown":
        return False, "Email provider is not trusted or unrecognized."

    return True, f"Valid email from {provider}."

