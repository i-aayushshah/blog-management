from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for the API.
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Blog API is running',
        'timestamp': '2024-01-01T00:00:00Z'
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_info(request):
    """
    API information endpoint.
    """
    return JsonResponse({
        'name': 'Blog API',
        'version': '1.0.0',
        'description': 'A full-stack blog application API',
        'endpoints': {
            'health': '/api/v1/health/',
            'auth': '/api/v1/auth/',
            'blog': '/api/v1/blog/',
        }
    })
