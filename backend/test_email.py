#!/usr/bin/env python
"""
Test script to verify email configuration.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test email configuration."""
    print("🔧 Testing Email Configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")

    try:
        # Send a test email
        send_mail(
            subject='Test Email from Blog Management',
            message='This is a test email to verify the email configuration is working correctly.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['aayushshah983@gmail.com'],
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        print("📧 Check your email inbox for the test message.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Make sure 2-Factor Authentication is enabled on your Gmail account")
        print("2. Generate an App Password from Google Account settings")
        print("3. Use the App Password (not your regular Gmail password)")
        print("4. Check that the .env file has the correct credentials")

if __name__ == "__main__":
    test_email_configuration()
