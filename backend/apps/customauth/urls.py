from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    UserRegistrationView,
    UserProfileView,
    ChangePasswordView,
    LogoutView,
    CustomTokenRefreshView
)

app_name = 'customauth'

urlpatterns = [
    # JWT Token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
