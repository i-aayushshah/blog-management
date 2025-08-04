#!/bin/bash

# Blog Management Backend Test Runner
# This script runs all tests with coverage reporting

set -e

echo "🧪 Running Blog Management Backend Tests"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not detected. Please activate it first."
    echo "Run: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
    exit 1
fi

# Install test dependencies if not already installed
echo "📦 Installing test dependencies..."
pip install -q coverage pytest pytest-django factory-boy faker

# Clean up previous coverage data
echo "🧹 Cleaning up previous coverage data..."
coverage erase

# Run tests with coverage
echo "🔍 Running tests with coverage..."
coverage run --source='.' manage.py test tests/ -v 2

# Generate coverage report
echo "📊 Generating coverage report..."
coverage report

# Generate HTML coverage report
echo "📄 Generating HTML coverage report..."
coverage html

# Check coverage threshold (80%)
COVERAGE=$(coverage report | tail -n 1 | awk '{print $4}' | sed 's/%//')
if (( $(echo "$COVERAGE >= 80" | bc -l) )); then
    print_status "Coverage is ${COVERAGE}% (above 80% threshold)"
else
    print_warning "Coverage is ${COVERAGE}% (below 80% threshold)"
fi

# Run specific test suites
echo ""
echo "🎯 Running specific test suites..."

echo "🔐 Authentication tests..."
python manage.py test tests.test_authentication -v 2

echo "📝 Blog tests..."
python manage.py test tests.test_blog -v 2

echo "🔧 Middleware tests..."
python manage.py test tests.test_middleware -v 2

# Run with pytest for more detailed output
echo ""
echo "🔬 Running with pytest..."
pytest tests/ -v --tb=short

# Performance tests (if available)
if [ -f "tests/test_performance.py" ]; then
    echo "⚡ Running performance tests..."
    python manage.py test tests.test_performance -v 2
fi

# Security tests (if available)
if [ -f "tests/test_security.py" ]; then
    echo "🔒 Running security tests..."
    python manage.py test tests.test_security -v 2
fi

# Integration tests (if available)
if [ -f "tests/test_integration.py" ]; then
    echo "🔗 Running integration tests..."
    python manage.py test tests.test_integration -v 2
fi

echo ""
print_status "All tests completed!"
echo ""
echo "📈 Coverage report available at: htmlcov/index.html"
echo "📋 Test results summary:"
echo "   - Authentication: ✅"
echo "   - Blog functionality: ✅"
echo "   - Middleware: ✅"
echo "   - Overall coverage: ${COVERAGE}%"
echo ""
echo "🚀 To view the HTML coverage report, open:"
echo "   file://$(pwd)/htmlcov/index.html"
