#!/usr/bin/env python
"""
Test script to verify resend verification endpoint.
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

def test_resend_verification():
    """Test resend verification endpoint."""
    print("🔧 Testing Resend Verification Endpoint...")

    # Test data
    test_email = "aayushshah817@gmail.com"

    # Test resend verification
    url = "http://localhost:8000/api/v1/auth/resend-verification/"
    data = {"email": test_email}

    try:
        response = requests.post(url, json=data)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")

        if response.status_code == 200:
            print("🎉 Resend verification endpoint is working!")
        else:
            print("❌ Resend verification endpoint failed")

    except Exception as e:
        print(f"❌ Error testing resend verification: {e}")

if __name__ == "__main__":
    test_resend_verification()
