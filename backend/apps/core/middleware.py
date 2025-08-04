import time
import logging
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from apps.authentication.jwt_utils import get_user_from_token, is_token_valid

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Custom JWT Authentication Middleware.
    """

    def process_request(self, request):
        """
        Process request and authenticate user using JWT token.
        """
        # Skip authentication for certain paths
        excluded_paths = [
            '/admin/',
            '/api/v1/health/',
            '/api/v1/info/',
            '/api/v1/auth/register/',
            '/api/v1/auth/login/',
            '/api/v1/auth/verify-email/',
            '/api/v1/auth/forgot-password/',
            '/api/v1/auth/reset-password/',
            '/api/v1/auth/resend-verification/',
            '/static/',
            '/media/',
        ]

        # Check if path should be excluded
        for excluded_path in excluded_paths:
            if request.path.startswith(excluded_path):
                return None

        # Get authorization header
        auth_header = get_authorization_header(request)

        if not auth_header:
            # For API endpoints, return 401
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'message': 'Authentication credentials were not provided.',
                    'error': 'authentication_required'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return None

        # Extract token
        auth_parts = auth_header.decode().split()

        if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'message': 'Invalid authentication header format.',
                    'error': 'invalid_auth_header'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return None

        token = auth_parts[1]

        # Validate token
        if not is_token_valid(token):
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'message': 'Invalid or expired token.',
                    'error': 'invalid_token'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return None

        # Get user from token
        try:
            user = get_user_from_token(token)
            request.user = user
        except Exception as e:
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'message': 'Invalid token.',
                    'error': 'invalid_token'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return None

        return None

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for logging HTTP requests.
    """

    def process_request(self, request):
        """
        Log request details.
        """
        request.start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.path} - User: {getattr(request.user, 'email', 'Anonymous')}")

        return None

    def process_response(self, request, response):
        """
        Log response details.
        """
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

            # Log response
            logger.info(
                f"Response: {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.3f}s - "
                f"User: {getattr(request.user, 'email', 'Anonymous')}"
            )

        return response

class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware for handling errors and exceptions.
    """

    def process_exception(self, request, exception):
        """
        Handle exceptions and return appropriate responses.
        """
        # Log the exception
        logger.error(f"Exception in {request.method} {request.path}: {str(exception)}")

        # For API requests, return JSON error response
        if request.path.startswith('/api/'):
            return JsonResponse({
                'message': 'An error occurred while processing your request.',
                'error': 'internal_server_error',
                'detail': str(exception) if settings.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # For other requests, let Django handle it
        return None

class CORSMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware for handling cross-origin requests.
    """

    def process_response(self, request, response):
        """
        Add CORS headers to response.
        """
        # Add CORS headers
        response['Access-Control-Allow-Origin'] = settings.FRONTEND_URL
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'

        return response

    def process_request(self, request):
        """
        Handle preflight OPTIONS requests.
        """
        if request.method == 'OPTIONS':
            response = JsonResponse({})
            response['Access-Control-Allow-Origin'] = settings.FRONTEND_URL
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            return response

        return None
