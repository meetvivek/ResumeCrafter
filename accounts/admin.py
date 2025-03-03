from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerification

class CustomUserAdmin(UserAdmin):
    """Admin customization for the CustomUser model."""

    ordering = ("-date_joined",)  # Sort by newest users first
    list_display = ("email", "first_name", "last_name", "date_joined")
    list_filter = ("date_joined",)
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ( "is_staff", "is_active", "is_superuser")}),
        ("Important Dates", {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )


class EmailVerificationAdmin(admin.ModelAdmin):
    """Admin customization for email verification."""

    list_display = ("user", "token", "is_verified", "created_at")
    list_filter = ("is_verified", "created_at")
    search_fields = ("user__email",)
    ordering = ("-created_at",)
    readonly_fields = ("token", "created_at")  # Prevent token modifications


# Register models in Django admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)
