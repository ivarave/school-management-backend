from django.urls import path, include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from django.contrib.auth import get_user_model
User = get_user_model()

urlpatterns = [
    path('register/', CreateUserView.as_view(), name= 'register'),
    path('token/',TokenObtainPairView.as_view(),name='get_token'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('api-auth/', include('rest_framework.urls')),
]