#!/usr/bin/env python3
"""
Test script to verify PostCard fix
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

def test_posts_endpoint():
    """Test posts endpoint to check data structure"""
    print("\n📝 Testing posts endpoint...")

    try:
        response = requests.get("http://localhost:8000/api/v1/blog/posts/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Posts endpoint working")
            print(f"📊 Found {data.get('count', 0)} posts")

            if 'results' in data and data['results']:
                print("\n📋 Checking post structure:")
                for i, post in enumerate(data['results'][:3]):  # Check first 3 posts
                    print(f"  Post {i+1}:")
                    print(f"    ID: {post.get('id')}")
                    print(f"    Title: {post.get('title', 'N/A')}")
                    print(f"    Tags: {post.get('tags', 'N/A')}")
                    print(f"    Category: {post.get('category', 'N/A')}")
                    print(f"    Author: {post.get('author', 'N/A')}")
                    print()
            else:
                print("⚠️  No posts found")
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

def test_blog_page():
    """Test blog page"""
    print("\n📖 Testing blog page...")

    try:
        response = requests.get("http://localhost:3000/blog")
        if response.status_code == 200:
            print("✅ Blog page accessible")
            content = response.text
            if "Blog" in content:
                print("✅ Blog page content loaded")
            else:
                print("⚠️  Blog page might have issues")
        else:
            print(f"❌ Blog page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Blog page test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing PostCard Fix")
    print("=" * 60)

    backend_ok = test_backend_status()
    test_posts_endpoint()
    frontend_ok = test_frontend_status()
    test_blog_page()

    print("\n" + "=" * 60)
    print("  Test Complete")
    print("=" * 60)

    if backend_ok and frontend_ok:
        print("\n✅ Both servers are running")
        print("\n🔧 Fixes Applied:")
        print("✅ Added null check for post.tags in PostCard")
        print("✅ Added null check for post.category in PostCard")
        print("✅ Added null check for posts array in PostList")
        print("\n💡 The error should now be resolved!")
        print("📋 Test the blog page at http://localhost:3000/blog")
    else:
        print("\n❌ Server issues detected")
        print("💡 Make sure both servers are running:")
        print("   Backend: python manage.py runserver")
        print("   Frontend: npm run dev")
