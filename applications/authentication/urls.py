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
    path('api/auth_test/', views.test, name='test'),
    path('api/find_by_nip/', views.find_user_by_nip, name='find_by_nip'),
]
