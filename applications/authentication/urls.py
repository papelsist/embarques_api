from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_user/', views.get_user, name='get_user'),
    path('api/get_usuario/', views.GetUser.as_view(), name='get_usuario'),
    path('api/find_by_nip/', views.find_user_by_nip, name='find_by_nip'),
    path('api/usuarios/', views.UsersListView.as_view(), name='usuarios'),
    path('api/usuarios/<int:pk>/', views.UserRetrieveView.as_view(), name='usuario_detail'),
    path('api/usuarios/create/', views.create_user, name='usuario_create'),
    path('api/usuarios/update/', views.update_user, name='usuario_update'),    
    path('api/usuarios/update_password/', views.update_password, name='usuario_update_password'),
    path('api/usuarios/find_user_by_username/', views.find_user_by_username, name='find_user_by_username'),
]
