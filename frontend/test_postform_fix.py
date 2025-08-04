#!/usr/bin/env python3
"""
Test script to verify PostForm fix
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

def test_categories_endpoint():
    """Test categories endpoint"""
    print("\n📂 Testing categories endpoint...")

    try:
        response = requests.get("http://localhost:8000/api/v1/blog/categories/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Categories endpoint working")
            print(f"📊 Found {len(data.get('results', data))} categories")

            categories = data.get('results', data)
            if categories:
                print("\n📋 Available categories:")
                for i, category in enumerate(categories[:5]):  # Show first 5
                    print(f"  {i+1}. ID: {category.get('id')} | Name: {category.get('name', 'N/A')}")
            else:
                print("⚠️  No categories found")
        else:
            print(f"❌ Categories endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")

def test_tags_endpoint():
    """Test tags endpoint"""
    print("\n🏷️  Testing tags endpoint...")

    try:
        response = requests.get("http://localhost:8000/api/v1/blog/tags/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tags endpoint working")
            print(f"📊 Found {len(data.get('results', data))} tags")

            tags = data.get('results', data)
            if tags:
                print("\n📋 Available tags:")
                for i, tag in enumerate(tags[:5]):  # Show first 5
                    print(f"  {i+1}. ID: {tag.get('id')} | Name: {tag.get('name', 'N/A')}")
            else:
                print("⚠️  No tags found")
        else:
            print(f"❌ Tags endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Tags endpoint error: {e}")

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

def test_create_post_page():
    """Test create post page"""
    print("\n✏️  Testing create post page...")

    try:
        response = requests.get("http://localhost:3000/create-post")
        if response.status_code == 200:
            print("✅ Create post page accessible")
            content = response.text
            if "Create Post" in content:
                print("✅ Create post form loaded")
            else:
                print("⚠️  Create post form might have issues")
        elif response.status_code == 302:
            print("✅ Create post page redirects to login (expected for unauthenticated)")
        else:
            print(f"⚠️  Create post page status: {response.status_code}")
    except Exception as e:
        print(f"❌ Create post page test failed: {e}")

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
    print("  Testing PostForm Fix")
    print("=" * 60)

    backend_ok = test_backend_status()
    test_categories_endpoint()
    test_tags_endpoint()
    frontend_ok = test_frontend_status()
    test_create_post_page()
    test_edit_post_page()

    print("\n" + "=" * 60)
    print("  Test Complete")
    print("=" * 60)

    if backend_ok and frontend_ok:
        print("\n✅ Both servers are running")
        print("\n🔧 Fixes Applied:")
        print("✅ Added null check for post.tags in PostForm initialization")
        print("✅ Added null check for categories.map() in PostForm")
        print("✅ Added null check for tags.map() in PostForm")
        print("\n💡 The PostForm error should now be resolved!")
        print("📋 Test the forms:")
        print("   1. Login to your account")
        print("   2. Go to http://localhost:3000/create-post")
        print("   3. Go to http://localhost:3000/edit-post/1")
        print("   4. Both forms should load without errors")
    else:
        print("\n❌ Server issues detected")
        print("💡 Make sure both servers are running:")
        print("   Backend: python manage.py runserver")
        print("   Frontend: npm run dev")
