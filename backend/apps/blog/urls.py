from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Placeholder URLs for blog endpoints
    # These will be implemented in future parts
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('categories/', views.categories, name='categories'),
    path('tags/', views.tags, name='tags'),
]
