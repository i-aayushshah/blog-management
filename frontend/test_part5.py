#!/usr/bin/env python
"""
Test Script for Part 5: Frontend Setup & Authentication
Tests the Next.js frontend application.
"""

import os
import sys
import requests
import time
import subprocess
import json

def check_frontend_server():
    """Check if the frontend server is running."""
    print("🔍 Checking frontend server...")

    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server is running on http://localhost:3000")
            return True
        else:
            print(f"❌ Frontend server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend server is not running: {e}")
        return False

def check_backend_server():
    """Check if the backend server is running."""
    print("🔍 Checking backend server...")

    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running on http://localhost:8000")
            return True
        else:
            print(f"❌ Backend server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend server is not running: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("\n🔍 Testing API endpoints...")

    # Test root endpoint
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

    # Test auth endpoints
    auth_endpoints = [
        "/api/v1/auth/register/",
        "/api/v1/auth/login/",
        "/api/v1/auth/check-auth/",
    ]

    for endpoint in auth_endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}")
            if response.status_code in [200, 405]:  # 405 is expected for GET on POST endpoints
                print(f"✅ {endpoint} accessible")
            else:
                print(f"❌ {endpoint} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")

def test_frontend_pages():
    """Test frontend pages."""
    print("\n🔍 Testing frontend pages...")

    pages = [
        ("/", "Home"),
        ("/login", "Login"),
        ("/register", "Register"),
        ("/blog", "Blog"),
    ]

    for path, name in pages:
        try:
            response = requests.get(f"http://localhost:3000{path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} page working")
            else:
                print(f"❌ {name} page failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} page error: {e}")

def test_environment():
    """Test environment configuration."""
    print("\n🔍 Testing environment configuration...")

    # Check if .env.local exists
    if os.path.exists(".env.local"):
        print("✅ .env.local file exists")

        with open(".env.local", "r") as f:
            content = f.read().strip()
            if "NEXT_PUBLIC_API_URL=" in content:
                print("✅ NEXT_PUBLIC_API_URL configured")
            else:
                print("❌ NEXT_PUBLIC_API_URL not found in .env.local")
    else:
        print("❌ .env.local file not found")

    # Check package.json dependencies
    if os.path.exists("package.json"):
        with open("package.json", "r") as f:
            data = json.load(f)
            dependencies = data.get("dependencies", {})
            dev_dependencies = data.get("devDependencies", {})

            required_deps = [
                "next", "react", "react-dom", "zustand", "axios", "react-hook-form", "react-hot-toast",
                "lucide-react", "@tailwindcss/typography"
            ]

            required_dev_deps = [
                "typescript", "tailwindcss"
            ]

            missing_deps = []
            for dep in required_deps:
                if dep not in dependencies:
                    missing_deps.append(dep)

            for dep in required_dev_deps:
                if dep not in dev_dependencies:
                    missing_deps.append(dep)

            if missing_deps:
                print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
            else:
                print("✅ All required dependencies installed")

def check_directory_structure():
    """Check if the required directory structure exists."""
    print("\n🔍 Checking directory structure...")

    required_dirs = [
        "app/(auth)/login",
        "app/(auth)/register",
        "app/(auth)/verify-email",
        "app/(auth)/forgot-password",
        "app/(auth)/reset-password",
        "app/blog",
        "app/profile",
        "app/create-post",
        "app/edit-post",
        "components/ui",
        "components/auth",
        "components/blog",
        "components/layout",
        "lib",
        "store",
        "types",
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
    else:
        print("✅ All required directories exist")

def check_components():
    """Check if required components exist."""
    print("\n🔍 Checking components...")

    required_files = [
        "components/ui/Button.tsx",
        "components/ui/Input.tsx",
        "components/ui/Textarea.tsx",
        "components/auth/LoginForm.tsx",
        "components/auth/RegisterForm.tsx",
        "components/auth/AuthProvider.tsx",
        "components/auth/ProtectedRoute.tsx",
        "components/layout/Navigation.tsx",
        "store/authStore.ts",
        "lib/api.ts",
        "lib/utils.ts",
        "types/index.ts",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required components exist")

def main():
    """Run all frontend tests."""
    print("🚀 Starting Part 5 Frontend Tests...")
    print("=" * 60)

    # Check directory structure
    check_directory_structure()

    # Check components
    check_components()

    # Test environment
    test_environment()

    # Check servers
    frontend_running = check_frontend_server()
    backend_running = check_backend_server()

    if backend_running:
        test_api_endpoints()

    if frontend_running:
        test_frontend_pages()

    print("\n" + "=" * 60)
    print("🎉 Frontend Tests Completed!")

    if frontend_running and backend_running:
        print("\n✅ Both servers are running!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
        print("\n📋 Manual Testing Steps:")
        print("1. Visit http://localhost:3000")
        print("2. Navigate to /register to create an account")
        print("3. Check backend console for verification email")
        print("4. Use verification link/token")
        print("5. Login with verified credentials")
        print("6. Test protected routes")
        print("7. Test logout functionality")
    else:
        print("\n❌ Some servers are not running")
        if not backend_running:
            print("💡 Start backend: cd backend && python manage.py runserver")
        if not frontend_running:
            print("💡 Start frontend: npm run dev")

    print("\nFeatures implemented:")
    print("• Next.js 14 with TypeScript and Tailwind CSS")
    print("• Zustand state management with persistence")
    print("• JWT authentication with localStorage")
    print("• React Hook Form with validation")
    print("• Toast notifications with react-hot-toast")
    print("• Responsive navigation with mobile menu")
    print("• Protected routes with authentication checks")
    print("• Modern UI components with Lucide icons")
    print("• API client with axios and interceptors")
    print("• Environment configuration")
    print("• Professional landing page")

if __name__ == "__main__":
    main()
