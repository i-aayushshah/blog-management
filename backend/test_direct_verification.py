#!/usr/bin/env python
"""
Test script to verify the direct verification flow without double verification.
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

def test_direct_verification():
    """Test the direct verification flow."""
    print("🔧 Testing Direct Verification Flow...")

    # Test data
    test_email = "aayushshah983@gmail.com"
    test_password = "SecurePass123!"

    # Step 1: Register a new user
    print("\n📝 Step 1: Registering new user...")
    register_url = "http://localhost:8000/api/v1/auth/register/"
    register_data = {
        "username": "testuser_direct_verify",
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

    # Step 2: Get the verification token from database
    print("\n🔑 Step 2: Getting verification token from database...")
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

    # Step 3: Test verification endpoint directly (simulating frontend call)
    print("\n✅ Step 3: Testing verification endpoint directly...")
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

    # Step 4: Check if user is now verified
    print("\n🔍 Step 4: Checking if user is verified...")
    try:
        user.refresh_from_db()
        if user.is_email_verified:
            print("✅ User is now verified in database")
        else:
            print("❌ User is still not verified")
    except Exception as e:
        print(f"❌ Error checking verification status: {e}")

    # Step 5: Try to login after verification
    print("\n🔐 Step 5: Testing login after verification...")
    login_url = "http://localhost:8000/api/v1/auth/login/"
    login_data = {
        "email": test_email,
        "password": test_password
    }

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
    print("1. Go to http://localhost:3000/register")
    print("2. Register a new account")
    print("3. Check your email for verification link")
    print("4. Click the verification link")
    print("5. You should be redirected to login page with success message")
    print("6. No 'Invalid or expired verification token' error should appear")

if __name__ == "__main__":
    test_direct_verification()
