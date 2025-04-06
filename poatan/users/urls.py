from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    UpdateProfileView,
    ChangePasswordView,
    DeleteProfileView
    
)
"""Url Endpoints for the User Login and Profile views"""
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete'),
]