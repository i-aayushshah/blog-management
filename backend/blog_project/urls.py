"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def root_view(request):
    """Root URL view that provides API information."""
    return JsonResponse({
        'message': 'Blog API is running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/v1/health/',
            'info': '/api/v1/info/',
            'auth': '/api/v1/auth/',
            'blog': '/api/v1/blog/',
            'admin': '/admin/',
        },
        'documentation': 'Check README.md for setup instructions'
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    # API URLs with versioning
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.authentication.urls', namespace='auth')),
    path('api/v1/blog/', include('apps.blog.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
