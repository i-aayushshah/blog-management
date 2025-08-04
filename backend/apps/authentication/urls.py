from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Placeholder URLs for authentication endpoints
    # These will be implemented in future parts
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('profile/', views.profile, name='profile'),
]
