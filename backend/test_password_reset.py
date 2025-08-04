#!/usr/bin/env python
"""
Test script to verify the password reset functionality.
"""

import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_password_reset():
    """Test the password reset flow."""
    print("🔧 Testing Password Reset Flow...")

    # Test data
    test_email = "aayushshah983@gmail.com"
    test_password = "SecurePass123!"
    new_password = "NewSecurePass456!"

    # Step 1: Register a new user (if not exists)
    print("\n📝 Step 1: Checking if user exists...")
    try:
        user = User.objects.get(email=test_email)
        print("✅ User exists")
    except User.DoesNotExist:
        print("❌ User not found, please register first")
        return

    # Step 2: Test forgot password endpoint
    print("\n📧 Step 2: Testing forgot password endpoint...")
    forgot_url = "http://localhost:8000/api/v1/auth/forgot-password/"
    forgot_data = {"email": test_email}

    try:
        response = requests.post(forgot_url, json=forgot_data)
        print(f"✅ Forgot Password Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Password reset email sent successfully")
        else:
            print("❌ Password reset email failed")
            return
    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        return

    # Step 3: Get the reset token from database
    print("\n🔑 Step 3: Getting reset token from database...")
    try:
        user.refresh_from_db()
        token = user.password_reset_token
        print(f"✅ Reset token: {token}")
        print(f"✅ Reset URL: http://localhost:3000/reset-password/{token}")
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return

    # Step 4: Test reset password endpoint
    print("\n✅ Step 4: Testing reset password endpoint...")
    reset_url = "http://localhost:8000/api/v1/auth/reset-password/"
    reset_data = {
        "token": token,
        "new_password": new_password
    }

    try:
        response = requests.post(reset_url, json=reset_data)
        print(f"✅ Reset Password Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Password reset successfully")
        else:
            print("❌ Password reset failed")
            return
    except Exception as e:
        print(f"❌ Reset password error: {e}")
        return

    # Step 5: Test login with new password
    print("\n🔐 Step 5: Testing login with new password...")
    login_url = "http://localhost:8000/api/v1/auth/login/"
    login_data = {
        "email": test_email,
        "password": new_password
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"✅ Login Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Successfully logged in with new password")
            jwt_token = response.json().get('token')
            print(f"✅ JWT Token: {jwt_token[:50]}...")
        else:
            print("❌ Login failed with new password")
    except Exception as e:
        print(f"❌ Login error: {e}")

    # Step 6: Test login with old password (should fail)
    print("\n🔐 Step 6: Testing login with old password (should fail)...")
    old_login_data = {
        "email": test_email,
        "password": test_password
    }

    try:
        response = requests.post(login_url, json=old_login_data)
        print(f"✅ Old Password Login Status: {response.status_code}")

        if response.status_code == 400:
            print("✅ Correctly failed with old password")
        else:
            print("❌ Should have failed with old password")
    except Exception as e:
        print(f"❌ Old password login error: {e}")

    print("\n🎯 Frontend Testing Instructions:")
    print("1. Go to http://localhost:3000/forgot-password")
    print("2. Enter your email address")
    print("3. Click 'Send Reset Link'")
    print("4. Check your email for the reset link")
    print("5. Click the reset link (should go to /reset-password/[token])")
    print("6. Enter new password and confirm")
    print("7. Click 'Reset Password'")
    print("8. You should be redirected to login page")
    print("9. Try logging in with the new password")

if __name__ == "__main__":
    test_password_reset()
