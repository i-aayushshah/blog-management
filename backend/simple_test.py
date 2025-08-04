#!/usr/bin/env python
"""
Simple Test Script - Matches the user's original example
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

def main():
    """Run the simple test as shown in the user's example."""
    print("🚀 Running Simple Test (User's Example)...")
    print("=" * 50)

    try:
        # Test User model
        print("🔍 Testing User model...")
        from apps.authentication.models import User

        # Clean up any existing test user
        User.objects.filter(email='test@example.com').delete()

        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created user: {user.get_full_name()}")

        # Test Post model
        print("\n🔍 Testing Post model...")
        from apps.blog.models import Post

        # Clean up any existing test post
        Post.objects.filter(title='Test Post').delete()

        post = Post.objects.create(
            title='Test Post',
            content='This is test content',
            author=user,
            status='published'
        )
        print(f"✅ Created post: {post.title}")
        print(f"✅ Post slug: {post.slug}")  # Should auto-generate from title

        print("\n" + "=" * 50)
        print("🎉 Simple Test Completed Successfully!")
        print(f"✅ User: {user.get_full_name()}")
        print(f"✅ Post: {post.title} (slug: {post.slug})")

        # Clean up
        post.delete()
        user.delete()
        print("✅ Test data cleaned up")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
