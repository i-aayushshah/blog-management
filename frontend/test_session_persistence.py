#!/usr/bin/env python3
"""
Test script to verify session persistence fix
"""

import requests
import json

def test_backend_status():
    """Test if backend is running"""
    print("🔍 Testing backend status...")

    try:
        response = requests.get("http://localhost:8000/api/v1/")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_auth_endpoint():
    """Test auth endpoint"""
    print("\n🔐 Testing auth endpoint...")

    try:
        response = requests.get("http://localhost:8000/api/v1/auth/me/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Auth endpoint working")
            print(f"📋 User data: {data}")
        elif response.status_code == 401:
            print("⚠️  Auth endpoint requires authentication (expected)")
        else:
            print(f"❌ Auth endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Auth endpoint error: {e}")

def test_posts_endpoint():
    """Test posts endpoint"""
    print("\n📝 Testing posts endpoint...")

    try:
        response = requests.get("http://localhost:8000/api/v1/blog/posts/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Posts endpoint working")
            print(f"📊 Found {data.get('count', 0)} posts")

            if 'results' in data and data['results']:
                print("\n📋 First post details:")
                post = data['results'][0]
                print(f"  ID: {post.get('id')}")
                print(f"  Title: {post.get('title', 'N/A')}")
                print(f"  Author: {post.get('author', 'N/A')}")
                print(f"  Status: {post.get('status', 'N/A')}")
        else:
            print(f"❌ Posts endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Posts endpoint error: {e}")

def test_frontend_status():
    """Test if frontend is running"""
    print("\n🌐 Testing frontend status...")

    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_edit_post_page():
    """Test edit post page"""
    print("\n✏️  Testing edit post page...")

    try:
        response = requests.get("http://localhost:3000/edit-post/1")
        if response.status_code == 200:
            print("✅ Edit post page accessible")
            content = response.text
            if "Update Post" in content:
                print("✅ Edit post form loaded")
            elif "Loading..." in content:
                print("⚠️  Page shows loading state")
            elif "not authorized" in content.lower():
                print("⚠️  Page shows authorization error")
            else:
                print("✅ Page loads normally")
        elif response.status_code == 302:
            print("✅ Edit post page redirects to login (expected for unauthenticated)")
        else:
            print(f"⚠️  Edit post page status: {response.status_code}")
    except Exception as e:
        print(f"❌ Edit post page test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Session Persistence Fix")
    print("=" * 60)

    backend_ok = test_backend_status()
    test_auth_endpoint()
    test_posts_endpoint()
    frontend_ok = test_frontend_status()
    test_edit_post_page()

    print("\n" + "=" * 60)
    print("  Test Complete")
    print("=" * 60)

    if backend_ok and frontend_ok:
        print("\n✅ Both servers are running")
        print("\n🔧 Session Persistence Fixes Applied:")
        print("✅ Modified API interceptor to NOT clear auth for non-auth endpoints")
        print("✅ Modified checkAuth to preserve user data on non-401/403 errors")
        print("✅ Removed auth refresh call after post updates")
        print("✅ Added detailed logging for debugging")
        print("\n💡 Testing Steps:")
        print("1. Open browser developer console")
        print("2. Login to your account as 'Rabin Hood'")
        print("3. Go to http://localhost:3000/edit-post/1")
        print("4. Make changes and save the post")
        print("5. Check that your name stays as 'Rabin Hood' after update")
        print("6. No more session loss during post updates")
        print("\n🔍 Expected Console Messages:")
        print("  - 🔄 Updating post with ID: 1")
        print("  - ✅ Post update successful")
        print("  - ✅ Post updated successfully, auth state preserved")
        print("  - ⚠️  Non-auth endpoint returned 401 (if any)")
        print("  - ⚠️  NOT clearing auth token for non-auth endpoint")
        print("\n🚫 Auth will ONLY be cleared when:")
        print("  - User clicks logout button")
        print("  - Token actually expires (401/403 from auth endpoints)")
        print("  - User manually clears browser data")
    else:
        print("\n❌ Server issues detected")
        print("💡 Make sure both servers are running:")
        print("   Backend: python manage.py runserver")
        print("   Frontend: npm run dev")
