#!/usr/bin/env python
"""
Test Script for Part 4: Blog API Endpoints
Tests all blog endpoints and functionality.
"""

import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

def get_auth_token():
    """Get JWT token for authenticated requests."""
    print("🔑 Getting authentication token...")

    # First, create a test user if it doesn't exist
    from apps.authentication.models import User
    from apps.blog.models import Category, Tag

    # Create test user
    user, created = User.objects.get_or_create(
        email='blogtest@example.com',
        defaults={
            'username': 'blogtest',
            'first_name': 'Blog',
            'last_name': 'Test',
            'is_email_verified': True
        }
    )

    if created:
        user.set_password('SecurePass123!')
        user.save()
        print(f"✅ Created test user: {user.email}")
    else:
        # Update password for existing user
        user.set_password('SecurePass123!')
        user.save()
        print(f"✅ Updated existing user: {user.email}")

    # Create test category and tags
    category, created = Category.objects.get_or_create(
        name='Technology',
        defaults={'description': 'Technology related posts'}
    )
    if created:
        print(f"✅ Created test category: {category.name}")

    tag1, created = Tag.objects.get_or_create(name='Python')
    tag2, created = Tag.objects.get_or_create(name='Django')
    if created:
        print(f"✅ Created test tags: Python, Django")

    # Login to get token
    url = "http://127.0.0.1:8000/api/v1/auth/login/"
    data = {
        "email": "blogtest@example.com",
        "password": "SecurePass123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"✅ Login response status: {response.status_code}")
        print(f"✅ Login response: {response.json()}")

        if response.status_code == 200:
            token = response.json()['token']
            print(f"✅ Authentication successful")
            return token, user, category, [tag1, tag2]
        else:
            print(f"❌ Authentication failed: {response.json()}")
            return None, None, None, None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None, None, None, None

def test_create_post(token, category, tags):
    """Test creating a blog post."""
    print("\n🔍 Testing Post Creation...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "My First Blog Post",
        "content": "This is the content of my first blog post. It contains some interesting information about Django and Python development.",
        "excerpt": "A brief introduction to Django development",
        "status": "published",
        "category_id": category.id,
        "tag_ids": [tags[0].id, tags[1].id]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"✅ Create Post Status: {response.status_code}")
        if response.status_code == 201:
            post_data = response.json()
            print(f"✅ Post created: {post_data.get('title', 'Unknown')}")
            print(f"✅ Post data keys: {list(post_data.keys())}")
            print(f"✅ Post ID: {post_data.get('id', 'Not found')}")
            return post_data.get('id')
        else:
            print(f"❌ Create Post Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Create Post Error: {e}")
        return None

def test_get_posts():
    """Test getting all published posts."""
    print("\n🔍 Testing Get All Posts...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/"

    try:
        response = requests.get(url)
        print(f"✅ Get Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} posts")
            print(f"✅ Pagination: {data['count']} total posts")
            return data['results'][0]['id'] if data['results'] else None
        else:
            print(f"❌ Get Posts Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Get Posts Error: {e}")
        return None

def test_get_post_detail(post_id):
    """Test getting a specific post."""
    print("\n🔍 Testing Get Post Detail...")

    url = f"http://127.0.0.1:8000/api/v1/blog/posts/{post_id}/"

    try:
        response = requests.get(url)
        print(f"✅ Get Post Detail Status: {response.status_code}")
        if response.status_code == 200:
            post_data = response.json()
            print(f"✅ Post details: {post_data['title']}")
            print(f"✅ Author: {post_data['author']['username']}")
            print(f"✅ Reading time: {post_data['reading_time']} minutes")
            return True
        else:
            print(f"❌ Get Post Detail Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Get Post Detail Error: {e}")
        return False

def test_update_post(token, post_id):
    """Test updating a post."""
    print("\n🔍 Testing Update Post...")

    url = f"http://127.0.0.1:8000/api/v1/blog/posts/{post_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Updated Blog Post Title",
        "content": "This is the updated content of my blog post. It now contains more detailed information about Django development and best practices.",
        "excerpt": "Updated excerpt with more details",
        "status": "published"
    }

    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"✅ Update Post Status: {response.status_code}")
        if response.status_code == 200:
            post_data = response.json()
            print(f"✅ Post updated: {post_data['title']}")
            return True
        else:
            print(f"❌ Update Post Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Update Post Error: {e}")
        return False

def test_my_posts(token):
    """Test getting user's own posts."""
    print("\n🔍 Testing Get My Posts...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/my_posts/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"✅ Get My Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} of my posts")
            return True
        else:
            print(f"❌ Get My Posts Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Get My Posts Error: {e}")
        return False

def test_search_posts():
    """Test searching posts."""
    print("\n🔍 Testing Search Posts...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/?search=Django"

    try:
        response = requests.get(url)
        print(f"✅ Search Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} posts matching 'Django'")
            return True
        else:
            print(f"❌ Search Posts Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Search Posts Error: {e}")
        return False

def test_pagination():
    """Test pagination."""
    print("\n🔍 Testing Pagination...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/?page=1&page_size=5"

    try:
        response = requests.get(url)
        print(f"✅ Pagination Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Page 1: {len(data['results'])} posts")
            print(f"✅ Total: {data['count']} posts")
            print(f"✅ Next page: {data['next'] is not None}")
            return True
        else:
            print(f"❌ Pagination Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Pagination Error: {e}")
        return False

def test_categories():
    """Test getting categories."""
    print("\n🔍 Testing Get Categories...")

    url = "http://127.0.0.1:8000/api/v1/blog/categories/"

    try:
        response = requests.get(url)
        print(f"✅ Get Categories Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} categories")
            if data['results']:
                category = data['results'][0]
                print(f"✅ Category: {category['name']} ({category['post_count']} posts)")
            return data['results'][0]['id'] if data['results'] else None
        else:
            print(f"❌ Get Categories Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Get Categories Error: {e}")
        return None

def test_tags():
    """Test getting tags."""
    print("\n🔍 Testing Get Tags...")

    url = "http://127.0.0.1:8000/api/v1/blog/tags/"

    try:
        response = requests.get(url)
        print(f"✅ Get Tags Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} tags")
            if data['results']:
                tag = data['results'][0]
                print(f"✅ Tag: {tag['name']} ({tag['post_count']} posts)")
            return data['results'][0]['id'] if data['results'] else None
        else:
            print(f"❌ Get Tags Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Get Tags Error: {e}")
        return None

def test_category_posts(category_id):
    """Test getting posts by category."""
    print("\n🔍 Testing Get Posts by Category...")

    url = f"http://127.0.0.1:8000/api/v1/blog/categories/{category_id}/posts/"

    try:
        response = requests.get(url)
        print(f"✅ Category Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} posts in category")
            return True
        else:
            print(f"❌ Category Posts Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Category Posts Error: {e}")
        return False

def test_tag_posts(tag_id):
    """Test getting posts by tag."""
    print("\n🔍 Testing Get Posts by Tag...")

    url = f"http://127.0.0.1:8000/api/v1/blog/tags/{tag_id}/posts/"

    try:
        response = requests.get(url)
        print(f"✅ Tag Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['results'])} posts with tag")
            return True
        else:
            print(f"❌ Tag Posts Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Tag Posts Error: {e}")
        return False

def test_publish_unpublish(token, post_id):
    """Test publish/unpublish functionality."""
    print("\n🔍 Testing Publish/Unpublish...")

    headers = {"Authorization": f"Bearer {token}"}

    # Test unpublish
    url = f"http://127.0.0.1:8000/api/v1/blog/posts/{post_id}/unpublish/"
    try:
        response = requests.post(url, headers=headers)
        print(f"✅ Unpublish Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Post unpublished successfully")
        else:
            print(f"❌ Unpublish Error: {response.json()}")
    except Exception as e:
        print(f"❌ Unpublish Error: {e}")

    # Test publish
    url = f"http://127.0.0.1:8000/api/v1/blog/posts/{post_id}/publish/"
    try:
        response = requests.post(url, headers=headers)
        print(f"✅ Publish Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Post published successfully")
            return True
        else:
            print(f"❌ Publish Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Publish Error: {e}")
        return False

def test_featured_posts():
    """Test getting featured posts."""
    print("\n🔍 Testing Featured Posts...")

    url = "http://127.0.0.1:8000/api/v1/blog/posts/featured/"

    try:
        response = requests.get(url)
        print(f"✅ Featured Posts Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data)} featured posts")
            return True
        else:
            print(f"❌ Featured Posts Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Featured Posts Error: {e}")
        return False

def test_authorization(token):
    """Test authorization (users can only edit their own posts)."""
    print("\n🔍 Testing Authorization...")

    # Try to update a post that doesn't belong to the user
    url = "http://127.0.0.1:8000/api/v1/blog/posts/999/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": "Unauthorized Update"}

    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"✅ Authorization Test Status: {response.status_code}")
        if response.status_code in [403, 404]:
            print("✅ Authorization working correctly (blocked unauthorized access)")
            return True
        else:
            print(f"❌ Authorization Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Authorization Error: {e}")
        return False

def cleanup_test_data():
    """Clean up test data."""
    print("\n🧹 Cleaning up test data...")

    from apps.blog.models import Post
    from apps.authentication.models import User

    try:
        # Delete test posts
        Post.objects.filter(author__email='blogtest@example.com').delete()
        print("✅ Test posts cleaned up")

        # Delete test user
        User.objects.filter(email='blogtest@example.com').delete()
        print("✅ Test user cleaned up")

    except Exception as e:
        print(f"❌ Cleanup Error: {e}")

def main():
    """Run all blog API tests."""
    print("🚀 Starting Part 4 Blog API Tests...")
    print("=" * 60)

    try:
        # Get authentication token
        token, user, category, tags = get_auth_token()
        if not token:
            print("❌ Cannot proceed without authentication token")
            return False

        # Test creating a post
        post_id = test_create_post(token, category, tags)
        if not post_id:
            print("❌ Cannot proceed without a test post")
            return False

        # Test getting all posts
        test_get_posts()

        # Test getting post detail
        test_get_post_detail(post_id)

        # Test updating post
        test_update_post(token, post_id)

        # Test getting user's posts
        test_my_posts(token)

        # Test search functionality
        test_search_posts()

        # Test pagination
        test_pagination()

        # Test categories
        category_id = test_categories()
        if category_id:
            test_category_posts(category_id)

        # Test tags
        tag_id = test_tags()
        if tag_id:
            test_tag_posts(tag_id)

        # Test publish/unpublish
        test_publish_unpublish(token, post_id)

        # Test featured posts
        test_featured_posts()

        # Test authorization
        test_authorization(token)

        print("\n" + "=" * 60)
        print("🎉 All Blog API Tests Completed!")
        print("\nAvailable endpoints:")
        print("• GET /api/v1/blog/posts/ - List all published posts")
        print("• GET /api/v1/blog/posts/{id}/ - Get post details")
        print("• POST /api/v1/blog/posts/ - Create new post (auth required)")
        print("• PUT /api/v1/blog/posts/{id}/ - Update post (auth required)")
        print("• DELETE /api/v1/blog/posts/{id}/ - Delete post (auth required)")
        print("• GET /api/v1/blog/posts/my_posts/ - Get user's posts (auth required)")
        print("• GET /api/v1/blog/posts/featured/ - Get featured posts")
        print("• POST /api/v1/blog/posts/{id}/publish/ - Publish post (auth required)")
        print("• POST /api/v1/blog/posts/{id}/unpublish/ - Unpublish post (auth required)")
        print("• GET /api/v1/blog/categories/ - List categories")
        print("• GET /api/v1/blog/categories/{id}/posts/ - Get posts by category")
        print("• GET /api/v1/blog/tags/ - List tags")
        print("• GET /api/v1/blog/tags/{id}/posts/ - Get posts by tag")

        print("\nFeatures implemented:")
        print("• Full CRUD operations for posts")
        print("• Authentication and authorization")
        print("• Search functionality (title, content, excerpt)")
        print("• Filtering by status, author, category, tags")
        print("• Pagination (10 posts per page)")
        print("• Slug generation from title")
        print("• Draft/Published status management")
        print("• Author permissions (only edit own posts)")
        print("• Category and tag relationships")
        print("• Reading time calculation")
        print("• Featured posts endpoint")
        print("• Publish/Unpublish actions")

        # Clean up test data
        cleanup_test_data()

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Django server is running: python manage.py runserver")
        print("2. Ensure all dependencies are installed")
        print("3. Check that migrations are applied")
        print("4. Verify authentication system is working")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
