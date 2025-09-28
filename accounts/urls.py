from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, login_view, ProfileView, UserListView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Admin user management endpoints
    path('admin/users/', UserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', UserDetailView.as_view(), name='admin-user-detail'),
]