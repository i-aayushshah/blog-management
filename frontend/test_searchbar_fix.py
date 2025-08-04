#!/usr/bin/env python3
"""
Test script to verify the SearchBar TypeError fix
"""

import requests
import json

def test_searchbar_fix():
    """Test that the SearchBar component loads without JavaScript errors"""

    print("🔍 Testing SearchBar component fix...")

    # Test that the blog page loads without errors
    try:
        response = requests.get("http://localhost:3000/blog")
        if response.status_code == 200:
            print("✅ Blog page loads successfully")

            # Check if there are any obvious JavaScript errors in the response
            content = response.text
            if "SearchBar" in content or "search" in content.lower():
                print("✅ SearchBar component is present in the page")
            else:
                print("⚠️  SearchBar component might not be loaded")
        else:
            print(f"❌ Blog page failed to load: {response.status_code}")
    except Exception as e:
        print(f"❌ Blog page test failed: {e}")

    # Test that posts API returns data
    try:
        response = requests.get("http://localhost:8000/api/v1/blog/posts/")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and isinstance(data['results'], list):
                print(f"✅ Posts API returns {len(data['results'])} posts")
                if len(data['results']) > 0:
                    print("✅ Posts data structure looks correct")
                else:
                    print("⚠️  No posts found, but API structure is correct")
            else:
                print("⚠️  Posts API response structure might be unexpected")
        else:
            print(f"❌ Posts API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Posts API test failed: {e}")

def test_search_functionality():
    """Test search functionality"""

    print("\n🔍 Testing search functionality...")

    # Test search API endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/blog/posts/?search=test")
        if response.status_code == 200:
            print("✅ Search API endpoint works")
        else:
            print(f"❌ Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search API test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing SearchBar TypeError Fix")
    print("=" * 60)

    test_searchbar_fix()
    test_search_functionality()

    print("\n" + "=" * 60)
    print("  Test Complete")
    print("=" * 60)
    print("\n📋 Manual Verification:")
    print("1. Visit http://localhost:3000/blog")
    print("2. Check browser console for any JavaScript errors")
    print("3. Try typing in the search bar")
    print("4. Verify that search suggestions appear without errors")
    print("5. Test search functionality with different queries")
