from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, SignInView
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
] 