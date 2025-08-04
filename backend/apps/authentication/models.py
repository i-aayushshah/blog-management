from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import BaseModel
from apps.core.utils import generate_verification_token
import uuid


class User(AbstractUser, BaseModel):
    """
    Custom User model extending Django's AbstractUser.
    Includes email verification, password reset, and profile fields.
    """

    # Override email field to make it unique
    email = models.EmailField(unique=True, verbose_name='Email Address')

    # Profile fields
    first_name = models.CharField(max_length=30, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Last Name')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Phone Number')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name='Profile Picture'
    )

    # Email verification fields
    is_email_verified = models.BooleanField(default=False, verbose_name='Email Verified')
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_expires = models.DateTimeField(blank=True, null=True)

    # Password reset fields
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)

    # Meta fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    # Use email as username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['is_email_verified']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username

    def get_short_name(self):
        """Return the short name of the user."""
        return self.first_name or self.username

    def generate_verification_token(self):
        """Generate a new email verification token."""
        token = generate_verification_token()
        self.email_verification_token = token
        self.email_verification_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save(update_fields=['email_verification_token', 'email_verification_expires'])
        return token

    def verify_email(self, token):
        """Verify email with the provided token."""
        if (self.email_verification_token == token and
            self.email_verification_expires and
            self.email_verification_expires > timezone.now()):
            self.is_email_verified = True
            self.email_verification_token = None
            self.email_verification_expires = None
            self.save(update_fields=['is_email_verified', 'email_verification_token', 'email_verification_expires'])
            return True
        return False

    def generate_password_reset_token(self):
        """Generate a new password reset token."""
        token = generate_verification_token()
        self.password_reset_token = token
        self.password_reset_expires = timezone.now() + timezone.timedelta(hours=1)
        self.save(update_fields=['password_reset_token', 'password_reset_expires'])
        return token

    def verify_password_reset_token(self, token):
        """Verify password reset token."""
        if (self.password_reset_token == token and
            self.password_reset_expires and
            self.password_reset_expires > timezone.now()):
            return True
        return False

    def clear_password_reset_token(self):
        """Clear password reset token after use."""
        self.password_reset_token = None
        self.password_reset_expires = None
        self.save(update_fields=['password_reset_token', 'password_reset_expires'])

    @property
    def is_verified(self):
        """Check if user's email is verified."""
        return self.is_email_verified

    @property
    def display_name(self):
        """Get display name for the user."""
        return self.get_full_name() or self.username
