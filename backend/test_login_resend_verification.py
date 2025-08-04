#!/usr/bin/env python
"""
Test script to verify the login page resend verification feature.
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

def test_login_resend_verification():
    """Test the login page resend verification feature."""
    print("🔧 Testing Login Page Resend Verification Feature...")

    # Test data
    test_email = "aayushshah983@gmail.com"
    test_password = "SecurePass123!"

    # Step 1: Register a new user
    print("\n📝 Step 1: Registering new user...")
    register_url = "http://localhost:8000/api/v1/auth/register/"
    register_data = {
        "username": "testuser_login_resend",
        "email": test_email,
        "password": test_password,
        "password_confirm": test_password,
        "first_name": "Test",
        "last_name": "User"
    }

    try:
        response = requests.post(register_url, json=register_data)
        print(f"✅ Register Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ User registered successfully")
        else:
            print(f"❌ Registration failed: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return

    # Step 2: Try to login with unverified email (this should trigger resend option)
    print("\n🔐 Step 2: Testing login with unverified email...")
    login_url = "http://localhost:8000/api/v1/auth/login/"
    login_data = {
        "email": test_email,
        "password": test_password
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"✅ Login Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 400 and "verify your email" in response.json().get('error', ''):
            print("✅ Correctly blocked unverified user from logging in")
            print("✅ This should show resend verification option on frontend")
        else:
            print("❌ Unexpected login response")
    except Exception as e:
        print(f"❌ Login error: {e}")

    # Step 3: Test resend verification from login page
    print("\n📧 Step 3: Testing resend verification...")
    resend_url = "http://localhost:8000/api/v1/auth/resend-verification/"
    resend_data = {"email": test_email}

    try:
        response = requests.post(resend_url, json=resend_data)
        print(f"✅ Resend Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Resend verification email sent successfully")
        else:
            print("❌ Resend verification failed")
    except Exception as e:
        print(f"❌ Resend error: {e}")

    # Step 4: Get the verification token and verify email
    print("\n🔑 Step 4: Getting verification token from database...")
    try:
        user = User.objects.get(email=test_email)
        token = user.email_verification_token
        print(f"✅ Verification token: {token}")
        print(f"✅ Verification URL: http://localhost:3000/verify-email/{token}")
    except User.DoesNotExist:
        print("❌ User not found in database")
        return
    except Exception as e:
        print(f"❌ Error getting token: {e}")
        return

    # Step 5: Verify email
    print("\n✅ Step 5: Verifying email...")
    verify_url = "http://localhost:8000/api/v1/auth/verify-email/"
    verify_data = {"token": token}

    try:
        response = requests.post(verify_url, json=verify_data)
        print(f"✅ Verify Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Email verified successfully")
        else:
            print("❌ Email verification failed")
    except Exception as e:
        print(f"❌ Verification error: {e}")

    # Step 6: Try to login again after verification
    print("\n🔐 Step 6: Testing login after verification...")
    try:
        response = requests.post(login_url, json=login_data)
        print(f"✅ Login Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("✅ Successfully logged in after verification")
            token = response.json().get('token')
            print(f"✅ JWT Token: {token[:50]}...")
        else:
            print("❌ Login failed after verification")
    except Exception as e:
        print(f"❌ Login error: {e}")

    # Cleanup
    print("\n🧹 Cleaning up test data...")
    try:
        User.objects.filter(email=test_email).delete()
        print("✅ Test user deleted")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

    print("\n🎯 Frontend Testing Instructions:")
    print("1. Go to http://localhost:3000/login")
    print("2. Try to login with an unverified email")
    print("3. You should see a yellow warning box with resend verification option")
    print("4. Click 'Resend Email' to send a new verification email")
    print("5. Check your email and click the verification link")
    print("6. Try logging in again - it should work now")

if __name__ == "__main__":
    test_login_resend_verification()
