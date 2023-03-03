"""URL-роутинг приложения API."""
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import SignupView, TokenObtainView
from api import views


app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    # path('v1/users/', UsersView.as_view(), name='users'),
]
