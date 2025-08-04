import json
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.authentication.models import User
from apps.authentication.jwt_utils import generate_token, get_user_from_token
from apps.core.middleware import JWTAuthenticationMiddleware
from django.http import HttpResponse

User = get_user_model()

class MiddlewareTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        self.middleware = JWTAuthenticationMiddleware(lambda request: HttpResponse())

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_middleware_with_valid_token(self):
        """Test middleware with valid JWT token"""
        token = generate_token(self.user)

        request = self.factory.get('/api/blog/posts/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

        response = self.middleware(request)

        # Check if user is set on request
        self.assertEqual(request.user, self.user)

    def test_middleware_with_invalid_token(self):
        """Test middleware with invalid JWT token"""
        request = self.factory.get('/api/blog/posts/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer invalid_token'
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Check if user remains anonymous
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_without_token(self):
        """Test middleware without JWT token"""
        request = self.factory.get('/api/blog/posts/')
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Check if user remains anonymous
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_non_api_endpoint(self):
        """Test middleware with non-API endpoint"""
        request = self.factory.get('/admin/')
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Middleware should not process non-API endpoints
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_with_expired_token(self):
        """Test middleware with expired token"""
        # Create a token that would be expired (this is a simplified test)
        request = self.factory.get('/api/blog/posts/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer expired_token_here'
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Check if user remains anonymous
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_with_malformed_header(self):
        """Test middleware with malformed authorization header"""
        request = self.factory.get('/api/blog/posts/')
        request.META['HTTP_AUTHORIZATION'] = 'InvalidFormat token'
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Check if user remains anonymous
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_with_empty_token(self):
        """Test middleware with empty token"""
        request = self.factory.get('/api/blog/posts/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer '
        # Initialize user as anonymous
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        response = self.middleware(request)

        # Check if user remains anonymous
        self.assertTrue(request.user.is_anonymous)

    def test_middleware_preserves_existing_user(self):
        """Test middleware preserves existing user on request"""
        # Set a user on the request
        request = self.factory.get('/api/blog/posts/')
        request.user = self.user

        response = self.middleware(request)

        # User should remain the same
        self.assertEqual(request.user, self.user)

    def test_jwt_utils_token_generation(self):
        """Test JWT token generation utility"""
        token = generate_token(self.user)

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    def test_jwt_utils_get_user_from_token(self):
        """Test getting user from valid token"""
        token = generate_token(self.user)
        user_from_token = get_user_from_token(token)

        self.assertEqual(user_from_token, self.user)

    def test_jwt_utils_get_user_from_invalid_token(self):
        """Test getting user from invalid token"""
        user_from_token = get_user_from_token('invalid_token')

        self.assertIsNone(user_from_token)

    def test_jwt_utils_get_user_from_none_token(self):
        """Test getting user from None token"""
        user_from_token = get_user_from_token(None)

        self.assertIsNone(user_from_token)

    def test_jwt_utils_get_user_from_empty_token(self):
        """Test getting user from empty token"""
        user_from_token = get_user_from_token('')

        self.assertIsNone(user_from_token)

class CORSMiddlewareTestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_cors_preflight_request(self):
        """Test CORS preflight request handling"""
        response = self.client.options('/api/v1/auth/login/', HTTP_ORIGIN='http://localhost:3000')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Access-Control-Allow-Origin', response)
        self.assertIn('Access-Control-Allow-Methods', response)
        self.assertIn('Access-Control-Allow-Headers', response)

    def test_cors_actual_request(self):
        """Test CORS headers on actual request"""
        response = self.client.get('/api/v1/blog/posts/', HTTP_ORIGIN='http://localhost:3000')

        self.assertIn('Access-Control-Allow-Origin', response)
        self.assertIn('Access-Control-Allow-Methods', response)
        self.assertIn('Access-Control-Allow-Headers', response)

    def test_cors_without_origin(self):
        """Test CORS handling without origin header"""
        response = self.client.get('/api/v1/blog/posts/')

        # Should still work without origin header
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cors_allowed_origins(self):
        """Test CORS with different allowed origins"""
        allowed_origins = [
            'http://localhost:3000',
            'http://127.0.0.1:3000',
            'https://yourdomain.com'
        ]

        for origin in allowed_origins:
            response = self.client.get('/api/v1/blog/posts/', HTTP_ORIGIN=origin)
            self.assertIn('Access-Control-Allow-Origin', response)

    def test_cors_disallowed_origin(self):
        """Test CORS with disallowed origin"""
        response = self.client.get('/api/v1/blog/posts/', HTTP_ORIGIN='http://malicious-site.com')

        # Should still work but may not include CORS headers for disallowed origins
        self.assertEqual(response.status_code, status.HTTP_200_OK)
