from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r'follow', FollowViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
