from django.urls import path
from .views import SignupView, LoginView, LogoutView, EmailVerificationView, ResendVerificationEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-email/<uuid:token>/", EmailVerificationView.as_view(), name="email-verify"),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="token_blacklist"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]
