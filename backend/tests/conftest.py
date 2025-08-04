import pytest
from django.conf import settings
from rest_framework.test import APIClient
from apps.authentication.models import User
from apps.blog.models import Post, Category, Tag

@pytest.fixture
def api_client():
    """Return an API client for testing"""
    return APIClient()

@pytest.fixture
def user():
    """Create and return a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        is_email_verified=True
    )

@pytest.fixture
def unverified_user():
    """Create and return an unverified test user"""
    return User.objects.create_user(
        username='unverifieduser',
        email='unverified@example.com',
        password='testpass123',
        first_name='Unverified',
        last_name='User',
        is_email_verified=False
    )

@pytest.fixture
def category():
    """Create and return a test category"""
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='Test category description'
    )

@pytest.fixture
def tag():
    """Create and return a test tag"""
    return Tag.objects.create(
        name='Test Tag',
        slug='test-tag'
    )

@pytest.fixture
def post(user, category, tag):
    """Create and return a test post"""
    post = Post.objects.create(
        title='Test Post',
        slug='test-post',
        content='This is a test post content.',
        excerpt='Test post excerpt',
        author=user,
        category=category,
        status='published'
    )
    post.tags.add(tag)
    return post

@pytest.fixture
def draft_post(user, category):
    """Create and return a draft test post"""
    return Post.objects.create(
        title='Draft Post',
        slug='draft-post',
        content='This is a draft post content.',
        excerpt='Draft post excerpt',
        author=user,
        category=category,
        status='draft'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client"""
    from apps.authentication.jwt_utils import generate_token
    token = generate_token(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client
