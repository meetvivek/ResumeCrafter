from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier."""

    def create_user(self, email, password, **extra_fields):
        """Create and return a regular user."""

        if not email:
            raise ValueError(_("The Email must be set"))
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValueError(_("Invalid password: ") + " ".join(e.messages))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields["is_staff"]:
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields["is_superuser"]:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
