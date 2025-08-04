import json
import jwt
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.authentication.models import User
from apps.authentication.jwt_utils import generate_token, get_user_from_token

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.register_url = reverse('auth:register')
        self.login_url = reverse('auth:login')
        self.check_auth_url = reverse('auth:check_auth')
        self.verify_email_url = reverse('auth:verify_email')
        self.resend_verification_url = reverse('auth:resend_verification')
        self.forgot_password_url = reverse('auth:forgot_password')
        self.reset_password_url = reverse('auth:reset_password')

        # Test user data
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Create a verified user
        self.verified_user = User.objects.create_user(
            username='verifieduser',
            email='verified@example.com',
            password='testpass123',
            first_name='Verified',
            last_name='User',
            is_email_verified=True
        )

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)

        # Check if user was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertFalse(user.is_verified)  # Should not be verified initially

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create user first
        User.objects.create_user(
            username='existinguser',
            email=self.user_data['email'],
            password='testpass123'
        )

        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create user first
        User.objects.create_user(
            username=self.user_data['username'],
            email='different@example.com',
            password='testpass123'
        )

        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(self.login_url, {
            'email': 'verified@example.com',
            'password': 'testpass123'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'verified@example.com')

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(self.login_url, {
            'email': 'verified@example.com',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_unverified_user(self):
        """Test login with unverified user"""
        # Create unverified user
        User.objects.create_user(
            username='unverifieduser',
            email='unverified@example.com',
            password='testpass123',
            is_email_verified=False
        )

        response = self.client.post(self.login_url, {
            'email': 'unverified@example.com',
            'password': 'testpass123'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_check_auth_authenticated(self):
        """Test check auth endpoint with authenticated user"""
        # Login first
        login_response = self.client.post(self.login_url, {
            'email': 'verified@example.com',
            'password': 'testpass123'
        })

        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.check_auth_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'verified@example.com')

    def test_check_auth_unauthenticated(self):
        """Test check auth endpoint without authentication"""
        response = self.client.get(self.check_auth_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_jwt_token_generation(self):
        """Test JWT token generation and validation"""
        token = generate_token(self.verified_user)

        # Verify token is not None
        self.assertIsNotNone(token)

        # Verify token can be decoded
        user_from_token = get_user_from_token(token)
        self.assertEqual(user_from_token, self.verified_user)

    def test_jwt_token_invalid(self):
        """Test JWT token validation with invalid token"""
        with self.assertRaises(jwt.InvalidTokenError):
            get_user_from_token('invalid_token')

    def test_forgot_password_success(self):
        """Test forgot password with valid email"""
        response = self.client.post(self.forgot_password_url, {
            'email': 'verified@example.com'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_forgot_password_invalid_email(self):
        """Test forgot password with invalid email"""
        response = self.client.post(self.forgot_password_url, {
            'email': 'nonexistent@example.com'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resend_verification_success(self):
        """Test resend verification with valid email"""
        # Create unverified user
        User.objects.create_user(
            username='unverifieduser',
            email='unverified@example.com',
            password='testpass123',
            is_email_verified=False
        )

        response = self.client.post(self.resend_verification_url, {
            'email': 'unverified@example.com'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_resend_verification_already_verified(self):
        """Test resend verification with already verified user"""
        response = self.client.post(self.resend_verification_url, {
            'email': 'verified@example.com'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_password_validation(self):
        """Test password validation during registration"""
        # Test weak password
        weak_password_data = self.user_data.copy()
        weak_password_data['password'] = '123'
        weak_password_data['email'] = 'weak@example.com'

        response = self.client.post(self.register_url, weak_password_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_email_validation(self):
        """Test email validation during registration"""
        # Test invalid email
        invalid_email_data = self.user_data.copy()
        invalid_email_data['email'] = 'invalid-email'

        response = self.client.post(self.register_url, invalid_email_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_username_validation(self):
        """Test username validation during registration"""
        # Test username that's too short
        invalid_username_data = self.user_data.copy()
        invalid_username_data['username'] = 'ab'  # Too short
        invalid_username_data['email'] = 'test2@example.com'

        response = self.client.post(self.register_url, invalid_username_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_model_str(self):
        """Test User model string representation"""
        self.assertEqual(str(self.verified_user), 'verified@example.com')

    def test_user_get_full_name(self):
        """Test User get_full_name method"""
        full_name = self.verified_user.get_full_name()
        self.assertEqual(full_name, 'Verified User')

    def test_user_get_short_name(self):
        """Test User get_short_name method"""
        short_name = self.verified_user.get_short_name()
        self.assertEqual(short_name, 'Verified')
