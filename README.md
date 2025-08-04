# Blog Management System

A full-stack blog management application built with Django REST Framework (backend) and Next.js (frontend).

## 🚀 Features

### Backend (Django)
- **Authentication**: JWT-based authentication with email verification
- **Blog Management**: CRUD operations for posts, categories, and tags
- **User Management**: User registration, login, password reset
- **API**: RESTful API with comprehensive documentation
- **Testing**: Comprehensive test suite with coverage reporting

### Frontend (Next.js)
- **Modern UI**: Responsive design with Tailwind CSS
- **State Management**: Zustand for client-side state
- **Authentication**: JWT token management with persistence
- **Blog Features**: Post creation, editing, publishing
- **Search & Filter**: Advanced search and filtering capabilities

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/blog-management.git
cd blog-management
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Run the development server
npm run dev
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=4

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Authentication
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
python manage.py test

# Run specific test files
python manage.py test tests.test_authentication
python manage.py test tests.test_blog
python manage.py test tests.test_middleware

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## 📚 API Documentation

Comprehensive API documentation is available in the `backend/API_DOCUMENTATION.md` file.

### Quick API Examples

#### Authentication
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Blog Posts
```bash
# Get all posts
curl http://localhost:8000/api/blog/posts/

# Create a new post (requires authentication)
curl -X POST http://localhost:8000/api/blog/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "This is my first blog post content.",
    "status": "draft"
  }'
```

## 🐳 Docker Setup

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Individual Dockerfiles

#### Backend
```bash
cd backend
docker build -t blog-backend .
docker run -p 8000:8000 blog-backend
```

#### Frontend
```bash
cd frontend
docker build -t blog-frontend .
docker run -p 3000:3000 blog-frontend
```

## 📁 Project Structure

```
blog-management/
├── backend/                 # Django backend
│   ├── apps/               # Django applications
│   │   ├── authentication/ # User authentication
│   │   ├── blog/          # Blog functionality
│   │   └── core/          # Core utilities
│   ├── blog_project/       # Django settings
│   ├── tests/             # Test suite
│   ├── media/             # Uploaded files
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── lib/               # Utility functions
│   ├── store/             # Zustand stores
│   └── package.json       # Node.js dependencies
├── docker-compose.yml      # Docker configuration
└── README.md              # This file
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Email Verification**: Required email verification for new accounts
- **Password Reset**: Secure password reset functionality
- **CORS Protection**: Configured CORS for cross-origin requests
- **Input Validation**: Comprehensive input validation and sanitization
- **Rate Limiting**: API rate limiting to prevent abuse

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**: Set production environment variables
2. **Database**: Configure production database (PostgreSQL recommended)
3. **Static Files**: Collect and serve static files
4. **Media Files**: Configure media file storage
5. **SSL**: Enable HTTPS with SSL certificates
6. **Monitoring**: Set up logging and monitoring
7. **Backup**: Configure database backups

### Deployment Options

#### Heroku
```bash
# Backend
heroku create your-backend-app
git push heroku main

# Frontend
heroku create your-frontend-app
git push heroku main
```

#### DigitalOcean
```bash
# Use DigitalOcean App Platform or Droplets
# Follow their deployment guides
```

#### AWS
```bash
# Use AWS Elastic Beanstalk, ECS, or EC2
# Follow AWS deployment documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/TypeScript
- Write comprehensive tests for new features
- Update documentation for API changes
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the API documentation in `backend/API_DOCUMENTATION.md`
- **Issues**: Report bugs and feature requests on GitHub
- **Email**: Contact support@blogmanagement.com

## 🙏 Acknowledgments

- Django REST Framework for the robust API framework
- Next.js for the modern React framework
- Tailwind CSS for the utility-first CSS framework
- Zustand for the lightweight state management
- JWT for secure authentication

## 📊 Performance

### Backend Performance
- **Database Queries**: Optimized with select_related and prefetch_related
- **Caching**: Redis caching for frequently accessed data
- **Pagination**: Efficient pagination for large datasets
- **Image Optimization**: Automatic image resizing and optimization

### Frontend Performance
- **Code Splitting**: Automatic code splitting with Next.js
- **Image Optimization**: Next.js Image component for optimized images
- **Lazy Loading**: Lazy loading for components and images
- **Bundle Optimization**: Optimized bundle sizes

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd backend
        python manage.py test
    - name: Run coverage
      run: |
        cd backend
        coverage run --source='.' manage.py test
        coverage report
```

## 📈 Monitoring

### Backend Monitoring
- Django Debug Toolbar for development
- Sentry for error tracking
- Custom logging for API requests
- Performance monitoring with Django Silk

### Frontend Monitoring
- Next.js built-in analytics
- Error boundary for React components
- Performance monitoring with Web Vitals
- User interaction tracking

---

**Happy Blogging! 📝✨**
