from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet,

router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r'comments', CommentViewSet, basename='followers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
