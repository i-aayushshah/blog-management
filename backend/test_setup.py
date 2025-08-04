#!/usr/bin/env python
"""
Test script to verify Django backend setup.
Run this after setting up the environment to check if everything is working.
"""

import os
import sys
import django
from django.conf import settings

def test_django_setup():
    """Test if Django is properly configured."""
    try:
        # Add the backend directory to Python path
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, backend_dir)

        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

        # Configure Django
        django.setup()

        print("✅ Django setup successful!")

        # Test settings
        print(f"✅ DEBUG mode: {settings.DEBUG}")
        print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)} apps")
        print(f"✅ CORS origins: {settings.CORS_ALLOWED_ORIGINS}")

        # Test imports
        from apps.core.models import BaseModel
        print("✅ Core models imported successfully")

        from apps.core.utils import generate_jwt_token, verify_jwt_token
        print("✅ Core utilities imported successfully")

        print("\n🎉 All tests passed! Django backend is ready.")
        print("\nAvailable endpoints:")
        print("• Root: http://localhost:8000/")
        print("• Health: http://localhost:8000/api/v1/health/")
        print("• Info: http://localhost:8000/api/v1/info/")
        print("• Admin: http://localhost:8000/admin/")
        print("\nNext steps:")
        print("1. Create .env file from env.example")
        print("2. Run: python manage.py makemigrations")
        print("3. Run: python manage.py migrate")
        print("4. Run: python manage.py createsuperuser")
        print("5. Run: python manage.py runserver")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the backend directory")
        print("2. Check if virtual environment is activated")
        print("3. Verify all dependencies are installed")
        print("4. Ensure .env file exists with required variables")
        return False

    return True

if __name__ == "__main__":
    test_django_setup()
