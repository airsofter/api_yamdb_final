from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (SignupView, TokenObtainView, UsersViewSet,
                    TitleViewSet, GenreViewSet, CategoryViewSet,
                    CommentViewSet, ReviewViewSet, SelfUser)


app_name = 'api'

router = DefaultRouter()

router.register(r"titles", TitleViewSet, basename="titles")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('users/', UsersViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('users/me/', SelfUser.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='user_me'),
    path('users/<str:username>/', UsersViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='users'),
]
