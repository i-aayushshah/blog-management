import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any

User = get_user_model()

def generate_jwt_token(user: User) -> str:
    """
    Generate JWT token for a user.

    Args:
        user: User instance

    Returns:
        JWT token string
    """
    payload = {
        'user_id': user.id,
        'email': user.email,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # 1 hour expiration
        'iat': datetime.datetime.utcnow(),
        'type': 'access'
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

# Alias for backward compatibility
generate_token = generate_jwt_token

def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dictionary

    Raises:
        jwt.InvalidTokenError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")

def get_user_from_token(token: str) -> Optional[User]:
    """
    Get user from JWT token.

    Args:
        token: JWT token string

    Returns:
        User instance or None if not found
    """
    try:
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')

        if not user_id:
            return None

        user = User.objects.get(id=user_id)
        return user

    except User.DoesNotExist:
        return None
    except jwt.InvalidTokenError:
        return None

def is_token_valid(token: str) -> bool:
    """
    Check if JWT token is valid.

    Args:
        token: JWT token string

    Returns:
        True if valid, False otherwise
    """
    try:
        decode_jwt_token(token)
        return True
    except jwt.InvalidTokenError:
        return False

def get_token_expiration(token: str) -> Optional[datetime.datetime]:
    """
    Get token expiration time.

    Args:
        token: JWT token string

    Returns:
        Expiration datetime or None if invalid
    """
    try:
        payload = decode_jwt_token(token)
        return datetime.datetime.fromtimestamp(payload['exp'])
    except jwt.InvalidTokenError:
        return None
