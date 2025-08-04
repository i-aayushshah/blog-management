import time
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .jwt_utils import generate_jwt_token, get_user_from_token
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, EmailVerificationSerializer,
    PasswordResetRequestSerializer, PasswordResetSerializer, UserProfileSerializer,
    UserProfileUpdateSerializer
)
from .services import (
    send_verification_email, send_password_reset_email,
    verify_email_token, verify_password_reset_token, clear_password_reset_token
)

User = get_user_model()

class RegisterView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.
        """
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            if send_verification_email(user):
                return Response({
                    'message': 'User registered successfully. Please check your email for verification.',
                    'user_id': user.id,
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'User registered but verification email could not be sent.',
                    'user_id': user.id,
                    'email': user.email
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate user and return JWT token.
        """
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT token
            token = generate_jwt_token(user)

            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            return Response({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_email_verified': user.is_email_verified
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Verify user email with token.
        """
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            user = verify_email_token(token)

            if user:
                return Response({
                    'message': 'Email verified successfully. You can now login.',
                    'user_id': user.id,
                    'email': user.email
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Invalid or expired verification token.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    """
    Password reset request endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send password reset email.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            if send_password_reset_email(user):
                return Response({
                    'message': 'Password reset email sent successfully. Please check your email.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Failed to send password reset email. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """
    Password reset endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Reset password with token.
        """
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            user = verify_password_reset_token(token)

            if user:
                # Set new password
                user.set_password(password)
                user.save(update_fields=['password'])

                # Clear reset token
                clear_password_reset_token(user)

                return Response({
                    'message': 'Password reset successfully. You can now login with your new password.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Invalid or expired reset token.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    User profile endpoint.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Get user profile.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update user profile.
        """
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'user': UserProfileSerializer(request.user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    """
    Get current user information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get current user data.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout user (client should discard token).
        """
        return Response({
            'message': 'Logout successful. Please discard your token.'
        }, status=status.HTTP_200_OK)

# Function-based views for additional endpoints

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    """
    Resend verification email.
    """
    email = request.data.get('email')

    if not email:
        return Response({
            'message': 'Email is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        if user.is_email_verified:
            return Response({
                'message': 'Email is already verified.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if send_verification_email(user):
            return Response({
                'message': 'Verification email sent successfully.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Failed to send verification email.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except User.DoesNotExist:
        return Response({
            'message': 'No user found with this email address.'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    """
    Check if user is authenticated.
    """
    return Response({
        'message': 'User is authenticated.',
        'user_id': request.user.id,
        'email': request.user.email
    }, status=status.HTTP_200_OK)
