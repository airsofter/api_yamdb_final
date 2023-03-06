from django.urls import path, include
from rest_framework import routers

from .views import (SignupView, TokenObtainView, UsersViewSet,
                    TitleViewSet, GenreViewSet, CategoryViewSet,)


router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
# router.register(r'auth/signup/', SignupView, basename='signup')
# router.register(r'auth/token/', TokenObtainView, basename='token_obtain')
router.register(r'users', UsersViewSet, basename='users_operation')
# router.register('users/me', UserMeViewSet, basename='user_me')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
]
