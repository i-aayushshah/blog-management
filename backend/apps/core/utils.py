import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_jwt_token(user_id, email):
    """
    Generate JWT token for user authentication.
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def verify_jwt_token(token):
    """
    Verify and decode JWT token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def send_email_verification(email, token, username):
    """
    Send email verification link to user.
    """
    subject = 'Verify your email address'
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    html_message = render_to_string('emails/email_verification.html', {
        'username': username,
        'verification_url': verification_url
    })

    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=html_message
    )


def send_password_reset_email(email, token, username):
    """
    Send password reset email to user.
    """
    subject = 'Reset your password'
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    html_message = render_to_string('emails/password_reset.html', {
        'username': username,
        'reset_url': reset_url
    })

    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=html_message
    )


def generate_verification_token():
    """
    Generate a random verification token.
    """
    import secrets
    return secrets.token_urlsafe(32)
