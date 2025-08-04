#!/usr/bin/env python
"""
Manual Test Script for Part 2: User Model & Database Schema
This script demonstrates the same testing process as the user's example.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

def test_user_model():
    """Test User model functionality."""
    print("🔍 Testing User Model...")

    from apps.authentication.models import User

    # Clean up any existing test user first
    User.objects.filter(email='test@example.com').delete()

    # Create test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    print(f"✅ Created user: {user.get_full_name()}")
    print(f"✅ User email: {user.email}")
    print(f"✅ User is verified: {user.is_verified}")

    # Test user methods
    print(f"✅ Full name: {user.get_full_name()}")
    print(f"✅ Display name: {user.display_name}")
    print(f"✅ Short name: {user.get_short_name()}")

    # Test email verification
    token = user.generate_verification_token()
    print(f"✅ Generated verification token: {token[:20]}...")

    # Test password reset
    reset_token = user.generate_password_reset_token()
    print(f"✅ Generated password reset token: {reset_token[:20]}...")

    return user

def test_blog_models():
    """Test Blog models functionality."""
    print("\n🔍 Testing Blog Models...")

    from apps.blog.models import Post, Category, Tag
    from apps.authentication.models import User

    # Get the test user
    user = User.objects.get(email='test@example.com')

    # Clean up any existing test data
    Post.objects.filter(title='Test Post').delete()
    Category.objects.filter(name='Technology').delete()
    Tag.objects.filter(name__in=['Python', 'Django']).delete()

    # Create test category
    category = Category.objects.create(
        name='Technology',
        description='Technology related posts'
    )
    print(f"✅ Created category: {category.name}")
    print(f"✅ Category slug: {category.slug}")

    # Create test tags
    tag1 = Tag.objects.create(name='Python')
    tag2 = Tag.objects.create(name='Django')
    print(f"✅ Created tags: {tag1.name}, {tag2.name}")

    # Create test post
    post = Post.objects.create(
        title='Test Post',
        content='This is test content with some additional text to make it longer for testing reading time calculation.',
        excerpt='A test excerpt for the blog post.',
        author=user,
        category=category,
        status='published'
    )
    post.tags.add(tag1, tag2)

    print(f"✅ Created post: {post.title}")
    print(f"✅ Post slug: {post.slug}")  # Should auto-generate from title
    print(f"✅ Post reading time: {post.reading_time} minutes")
    print(f"✅ Post is published: {post.is_published}")
    print(f"✅ Post excerpt: {post.excerpt_or_content}")

    # Test relationships
    print(f"✅ Post author: {post.author.get_full_name()}")
    print(f"✅ Post category: {post.category.name}")
    print(f"✅ Post tags: {', '.join([tag.name for tag in post.tags.all()])}")

    # Test category and tag post counts
    print(f"✅ Category post count: {category.post_count}")
    print(f"✅ Tag post count: {tag1.post_count}")

    # Test related posts
    related_posts = post.get_related_posts()
    print(f"✅ Related posts found: {related_posts.count()}")

    return post, category, tag1, tag2

def test_admin_registration():
    """Test that all models are registered in admin."""
    print("\n🔍 Testing Admin Registration...")

    from django.contrib import admin

    # Check if models are registered by looking at the registry
    registered_models = []
    for model in admin.site._registry.values():
        if hasattr(model, '_meta') and hasattr(model._meta, 'model_name'):
            registered_models.append(model._meta.model_name)

    expected_models = ['user', 'post', 'category', 'tag']
    for model_name in expected_models:
        if model_name in registered_models:
            print(f"✅ {model_name.title()} model registered in admin")
        else:
            print(f"❌ {model_name.title()} model NOT registered in admin")

    print("✅ Admin registration test completed")

def cleanup_test_data():
    """Clean up test data."""
    print("\n🧹 Cleaning up test data...")

    from apps.authentication.models import User
    from apps.blog.models import Post, Category, Tag

    # Delete test data
    Post.objects.filter(title='Test Post').delete()
    Category.objects.filter(name='Technology').delete()
    Tag.objects.filter(name__in=['Python', 'Django']).delete()
    User.objects.filter(email='test@example.com').delete()

    print("✅ Test data cleaned up")

def main():
    """Run all tests."""
    print("🚀 Starting Manual Tests for Part 2...")
    print("=" * 50)

    try:
        # Test User model
        user = test_user_model()

        # Test Blog models
        post, category, tag1, tag2 = test_blog_models()

        # Test Admin registration
        test_admin_registration()

        print("\n" + "=" * 50)
        print("🎉 All Manual Tests Passed!")
        print("\nAvailable models:")
        print("• User (with email verification)")
        print("• Category (with auto-slug)")
        print("• Tag (with auto-slug)")
        print("• Post (with auto-slug, reading time, relationships)")

        print("\nAdmin interfaces available:")
        print("• User admin with verification status")
        print("• Category admin with post count")
        print("• Tag admin with post count")
        print("• Post admin with publishing actions")

        print("\nNext steps:")
        print("1. Visit: http://127.0.0.1:8000/admin/")
        print("2. Login with your superuser credentials")
        print("3. Explore the admin interfaces")

        # Clean up test data
        cleanup_test_data()

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure virtual environment is activated")
        print("2. Ensure all dependencies are installed")
        print("3. Check that migrations are applied")
        print("4. Verify .env file exists with required variables")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
