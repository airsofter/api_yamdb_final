"""Обработчики приложения API."""
from rest_framework import permissions, viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer, ReviewSerializer

from reviews.models import Genre, Category, Title, Review, Comment

from .serializers import (
    SignupSerializer,
    TokenObtainSerializer,
    UsersSerializer,
)
from users.models import User
from .permissions import AuthorizedOrModeratorPermission


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений"""
    serializer_class = TitleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorizedOrModeratorPermission,
    )

    def get_post(self):
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class SignupView(generics.CreateAPIView):
    """Обработчик для регистрации пользователей."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'username': user.username,
                'email': user.email,
            },
            status=status.HTTP_200_OK,
            headers=headers
        )


class TokenObtainView(generics.GenericAPIView):
    """Обработчик для получения токена по коду подтверждения."""
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User.objects.all(),
            username=serializer.validated_data['username']
        )
        if (
            user.password
            == serializer.validated_data['confirmation_code']
        ):
            user.password = ''
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Обработчик для модели User."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me')
    def self_user(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'self_user':
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]
