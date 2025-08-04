import uuid
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()

def generate_verification_token() -> str:
    """
    Generate a secure verification token using UUID4.

    Returns:
        Secure token string
    """
    return str(uuid.uuid4())

def send_verification_email(user: User) -> bool:
    """
    Send email verification email to user.

    Args:
        user: User instance

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Generate verification token
        token = generate_verification_token()
        user.email_verification_token = token
        user.email_verification_expires = timezone.now() + timezone.timedelta(hours=24)
        user.save(update_fields=['email_verification_token', 'email_verification_expires'])

        # Email template context
        context = {
            'user': user,
            'verification_url': f"{settings.FRONTEND_URL}/verify-email?token={token}",
            'token': token,
            'expires_in': '24 hours'
        }

        # Render email templates
        subject = render_to_string('authentication/email/verification_subject.txt', context).strip()
        html_message = render_to_string('authentication/email/verification_email.html', context)
        plain_message = render_to_string('authentication/email/verification_email.txt', context)

        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )

        print(f"📧 Verification email sent to {user.email}")
        print(f"🔑 Verification token: {token}")

        return True

    except Exception as e:
        print(f"❌ Error sending verification email: {e}")
        return False

def send_password_reset_email(user: User) -> bool:
    """
    Send password reset email to user.

    Args:
        user: User instance

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Generate password reset token
        token = generate_verification_token()
        user.password_reset_token = token
        user.password_reset_expires = timezone.now() + timezone.timedelta(hours=1)
        user.save(update_fields=['password_reset_token', 'password_reset_expires'])

        # Email template context
        context = {
            'user': user,
            'reset_url': f"{settings.FRONTEND_URL}/reset-password?token={token}",
            'token': token,
            'expires_in': '1 hour'
        }

        # Render email templates
        subject = render_to_string('authentication/email/password_reset_subject.txt', context).strip()
        html_message = render_to_string('authentication/email/password_reset_email.html', context)
        plain_message = render_to_string('authentication/email/password_reset_email.txt', context)

        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )

        print(f"📧 Password reset email sent to {user.email}")
        print(f"🔑 Reset token: {token}")

        return True

    except Exception as e:
        print(f"❌ Error sending password reset email: {e}")
        return False

def verify_email_token(token: str) -> Optional[User]:
    """
    Verify email verification token.

    Args:
        token: Verification token

    Returns:
        User instance if valid, None otherwise
    """
    try:
        user = User.objects.get(
            email_verification_token=token,
            email_verification_expires__gt=timezone.now(),
            is_email_verified=False
        )

        # Mark email as verified
        user.is_email_verified = True
        user.email_verification_token = None
        user.email_verification_expires = None
        user.save(update_fields=['is_email_verified', 'email_verification_token', 'email_verification_expires'])

        return user

    except User.DoesNotExist:
        return None

def verify_password_reset_token(token: str) -> Optional[User]:
    """
    Verify password reset token.

    Args:
        token: Password reset token

    Returns:
        User instance if valid, None otherwise
    """
    try:
        user = User.objects.get(
            password_reset_token=token,
            password_reset_expires__gt=timezone.now()
        )
        return user

    except User.DoesNotExist:
        return None

def clear_password_reset_token(user: User) -> None:
    """
    Clear password reset token for user.

    Args:
        user: User instance
    """
    user.password_reset_token = None
    user.password_reset_expires = None
    user.save(update_fields=['password_reset_token', 'password_reset_expires'])
