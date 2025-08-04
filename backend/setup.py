#!/usr/bin/env python
"""
Setup script for Django backend.
This script automates the initial setup process.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path('.env')
    env_example = Path('env.example')

    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()

            # Generate random secret keys
            import secrets
            django_secret = secrets.token_urlsafe(50)
            jwt_secret = secrets.token_urlsafe(50)

            # Replace placeholder values
            content = content.replace('your-django-secret-key-here', django_secret)
            content = content.replace('your-jwt-secret-key-here', jwt_secret)

            with open(env_file, 'w') as f:
                f.write(content)

            print("✅ .env file created with generated secret keys")
            print("⚠️  Please update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env file")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("❌ env.example file not found")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Django backend...")

    # Check if we're in the backend directory
    if not os.path.exists('manage.py'):
        print("❌ Please run this script from the backend directory")
        return False

    # Create .env file
    if not create_env_file():
        return False

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False

    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating initial migrations"):
        return False

    if not run_command("python manage.py migrate", "Applying migrations"):
        return False

    # Test the setup
    if not run_command("python test_setup.py", "Testing setup"):
        return False

    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("3. Access admin panel: http://localhost:8000/admin")
    print("4. Test API endpoints: http://localhost:8000/api/v1/health/")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
