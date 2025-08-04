import time
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, EmailVerificationSerializer,
    PasswordResetRequestSerializer, PasswordResetSerializer, UserProfileSerializer,
    UserProfileUpdateSerializer
)
from .services import (
    send_verification_email, send_password_reset_email,
    verify_email_token, verify_password_reset_token, clear_password_reset_token
)
from .jwt_utils import generate_jwt_token

class RegisterView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            send_verification_email(user)

            return Response({
                'message': 'User registered successfully. Please check your email for verification.',
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
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Check if user is verified
            if not user.is_email_verified:
                return Response({
                    'error': 'Please verify your email before logging in.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT token
            token = generate_jwt_token(user)

            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']

            # Verify email
            success = verify_email_token(token)
            if success:
                return Response({
                    'message': 'Email verified successfully. You can now login.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid or expired verification token.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    """
    Forgot password endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)
                send_password_reset_email(user)

                return Response({
                    'message': 'Password reset email sent successfully.'
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({
                    'error': 'User not found.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    """
    Reset password endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            # Verify reset token and update password
            success = verify_password_reset_token(token, new_password)
            if success:
                return Response({
                    'message': 'Password reset successfully.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid or expired reset token.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    User profile endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    """
    Get current user information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # In a real application, you might want to blacklist the token
        # For now, we'll just return a success message
        return Response({
            'message': 'Logged out successfully.'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    """
    Resend verification email endpoint.
    """
    email = request.data.get('email')
    if not email:
        return Response({
            'error': 'Email is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.is_email_verified:
            return Response({
                'error': 'Email is already verified.'
            }, status=status.HTTP_400_BAD_REQUEST)

        send_verification_email(user)
        return Response({
            'message': 'Verification email sent successfully.'
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({
            'error': 'User not found.'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    """
    Check authentication status endpoint.
    """
    return Response({
        'message': 'Authentication system is working.'
    }, status=status.HTTP_200_OK)
