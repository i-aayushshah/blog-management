#!/usr/bin/env python
"""
Test runner script for the Blog Management Backend
Runs all tests with coverage reporting
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Run the test suite with coverage"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    # Run tests
    failures = test_runner.run_tests([
        'tests.test_authentication',
        'tests.test_blog',
        'tests.test_middleware',
    ])

    return failures

if __name__ == '__main__':
    failures = run_tests()
    sys.exit(bool(failures))
