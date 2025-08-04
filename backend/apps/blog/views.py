from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def posts(request):
    """
    Blog posts endpoint (placeholder).
    """
    return JsonResponse({
        'message': 'Blog posts endpoint - to be implemented',
        'status': 'placeholder'
    })


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def post_detail(request, post_id):
    """
    Individual blog post endpoint (placeholder).
    """
    return JsonResponse({
        'message': f'Blog post {post_id} endpoint - to be implemented',
        'status': 'placeholder'
    })


@csrf_exempt
@require_http_methods(["GET"])
def categories(request):
    """
    Blog categories endpoint (placeholder).
    """
    return JsonResponse({
        'message': 'Blog categories endpoint - to be implemented',
        'status': 'placeholder'
    })


@csrf_exempt
@require_http_methods(["GET"])
def tags(request):
    """
    Blog tags endpoint (placeholder).
    """
    return JsonResponse({
        'message': 'Blog tags endpoint - to be implemented',
        'status': 'placeholder'
    })
