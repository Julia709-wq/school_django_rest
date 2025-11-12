from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from users.views import PaymentListAPIView, UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

