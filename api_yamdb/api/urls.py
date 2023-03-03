"""URL-роутинг приложения API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SignupView, TokenObtainView, UsersViewSet

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users_operation')
# router.register('users/me', UserMeViewSet, basename='user_me')

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('v1/', include(router.urls)),
]
