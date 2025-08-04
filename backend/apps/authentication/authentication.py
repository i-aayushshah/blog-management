from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from .jwt_utils import get_user_from_token

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for Django REST Framework.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return None

        # Extract the token
        token = auth_header.split(' ')[1]

        try:
            # Get user from token
            user = get_user_from_token(token)
            if user and user.is_active:
                return (user, token)
            else:
                raise exceptions.AuthenticationFailed('Invalid token or user inactive')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

    def authenticate_header(self, request):
        """
        Return a string to be used as a value for the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer realm="api"'
