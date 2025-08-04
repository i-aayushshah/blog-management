from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),

    # User profile endpoints
    path('me/', views.UserMeView.as_view(), name='me'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('check-auth/', views.check_auth, name='check_auth'),
]
