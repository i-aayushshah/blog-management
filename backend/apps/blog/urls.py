from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'blog'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
