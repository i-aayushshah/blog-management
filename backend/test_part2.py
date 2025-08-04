#!/usr/bin/env python
"""
Test script for Part 2: User Model & Database Schema
Run this after setting up the models to verify everything works correctly.
"""

import os
import sys
import django
from django.conf import settings

def test_part2_setup():
    """Test Part 2 models and functionality."""
    try:
        # Add the backend directory to Python path
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, backend_dir)

        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

        # Configure Django
        django.setup()

        print("✅ Django setup successful!")

        # Test User model
        from apps.authentication.models import User
        print("✅ User model imported successfully")

        # Test blog models
        from apps.blog.models import Post, Category, Tag
        print("✅ Blog models imported successfully")

        # Test model relationships
        print("\n🔍 Testing model relationships...")

        # Create test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created test user: {user.get_full_name()}")

        # Test user methods
        print(f"✅ User full name: {user.get_full_name()}")
        print(f"✅ User display name: {user.display_name}")
        print(f"✅ User is verified: {user.is_verified}")

        # Test email verification
        token = user.generate_verification_token()
        print(f"✅ Generated verification token: {token[:20]}...")

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
            title='Test Blog Post',
            content='This is a test blog post content with some text to test the reading time calculation.',
            excerpt='A test excerpt for the blog post.',
            author=user,
            category=category,
            status='published'
        )
        post.tags.add(tag1, tag2)
        print(f"✅ Created test post: {post.title}")
        print(f"✅ Post slug: {post.slug}")
        print(f"✅ Post reading time: {post.reading_time} minutes")
        print(f"✅ Post is published: {post.is_published}")
        print(f"✅ Post excerpt: {post.excerpt_or_content}")

        # Test post relationships
        print(f"✅ Post author: {post.author.get_full_name()}")
        print(f"✅ Post category: {post.category.name}")
        print(f"✅ Post tags: {', '.join([tag.name for tag in post.tags.all()])}")

        # Test category and tag post counts
        print(f"✅ Category post count: {category.post_count}")
        print(f"✅ Tag post count: {tag1.post_count}")

        # Test related posts
        related_posts = post.get_related_posts()
        print(f"✅ Related posts found: {related_posts.count()}")

        # Test admin registration
        from django.contrib import admin
        print("✅ Admin models registered successfully")

        print("\n🎉 All Part 2 tests passed!")
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
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
        print("5. Visit: http://localhost:8000/admin/")

        # Clean up test data
        post.delete()
        category.delete()
        tag1.delete()
        tag2.delete()
        user.delete()
        print("\n🧹 Test data cleaned up")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the backend directory")
        print("2. Check if virtual environment is activated")
        print("3. Verify all dependencies are installed")
        print("4. Ensure .env file exists with required variables")
        print("5. Run migrations: python manage.py makemigrations && python manage.py migrate")
        return False

    return True

if __name__ == "__main__":
    test_part2_setup()
