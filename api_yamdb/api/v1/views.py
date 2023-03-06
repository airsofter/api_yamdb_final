"""Обработчики приложения API."""
from rest_framework import permissions, viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AuthorOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

from reviews.models import Genre, Category, Title, Review, Comment

from api.serializers import (
    SignupSerializer,
    TokenObtainSerializer,
    UsersSerializer,
)
from users.models import User
from api.permissions import AuthorizedOrModeratorPermission
from core.send_mail import send_mail


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
        AuthorOrReadOnly,
    )

    def get_post(self):
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


# class FollowViewSet(viewsets.ModelViewSet):
#     """Вьюсет Follow"""
#     serializer_class = FollowSerializer
#     filter_backends = (SearchFilter,)
#     search_fields = ('following__username',)

#     def get_queryset(self):
#         return self.request.user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

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
