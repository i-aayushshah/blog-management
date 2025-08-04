import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with validation.
    """
    email = serializers.EmailField(
        validators=[
            EmailValidator(),
            UniqueValidator(queryset=User.objects.all(), message="A user with this email already exists.")
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="A user with this username already exists.")
        ],
        min_length=3,
        max_length=30
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate_password(self, value):
        """
        Validate password strength.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        # Additional custom validation
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate login credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid credentials.')
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')

        return attrs

class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField(max_length=100)

    def validate_token(self, value):
        """
        Validate verification token.
        """
        if not value:
            raise serializers.ValidationError("Verification token is required.")
        return value

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate email exists.
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset.
    """
    token = serializers.CharField(max_length=100)
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate_password(self, value):
        """
        Validate password strength.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        # Additional custom validation
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                 'profile_picture', 'is_email_verified', 'date_joined', 'last_login']
        read_only_fields = ['id', 'email', 'is_email_verified', 'date_joined', 'last_login']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'profile_picture']

    def validate_username(self, value):
        """
        Validate username uniqueness.
        """
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
