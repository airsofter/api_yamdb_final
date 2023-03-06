"""URL-роутинг приложения API."""
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


app_name = 'api'

urlpatterns = [
    path('v1/', include('api.v1.urls')),
]
