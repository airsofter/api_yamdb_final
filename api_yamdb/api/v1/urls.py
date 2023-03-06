from django.urls import path, include
from rest_framework import routers

from .views import (SignupView, TokenObtainView,
                    CategoryViewSet, GenreViewSet,
                    TitleViewSet)


router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
# router.register(r'follow', FollowViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/signup/', SignupView.as_view(), name='signup'),
    path(r'auth/token/', TokenObtainView.as_view(),
         name='token_obtain'),
]
