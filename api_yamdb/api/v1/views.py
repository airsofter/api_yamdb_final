"""Обработчики приложения API."""
import random
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import generics, status, viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from core.pagination import UsersPagination
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (SignupSerializer, TokenObtainSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleRetrieveSerializer, TitleWriteSerializer,
                          ReviewSerializer, UsersSerializer, CommentSerializer)
from .permissions import AdminOnlyPermission, AuthorizedOrModeratorPermission
from users.models import User
from reviews.models import Genre, Category, Title, Review, Comment
from core.data_hash import hash_sha254


class SelfUser(viewsets.ViewSet):
    """Класс для операций по эндпоинту ('api/v1/users/me')."""

    permission_classes = [permissions.IsAuthenticated, ]
    
    def retrieve(self, request, pk=None):
        """Возвращает пользователя сделавшего запрос."""
        
        user = User.objects.get(username=request.user.username)
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    
    def partial_update(self, request):
        """Метод для PATCH запрсов на эндпоинт ('api/v1/users/me')."""
        
        data = request.data.copy()
        data.pop('role', None)
        user = User.objects.get(username=request.user.username)
        serializer = UsersSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Общий класс для CategoryViewSet и GenreViewSet."""
    # permission_classes = [IsAdminOrReadOnlyPermission]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


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
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AuthorizedOrModeratorPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'year', 'name')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleRetrieveSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (AdminOnlyPermission,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorizedOrModeratorPermission,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignupView(generics.CreateAPIView):
    """Обработчик для регистрации пользователей."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data
        ,
            status=status.HTTP_200_OK,
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # errors = {}
        # for field, error_list in serializer.errors.items():
        #     errors[field] = [str(e) for e in error_list]
        # return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(generics.GenericAPIView):
    """Обработчик для получения токена по коду подтверждения."""
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username'))
            token = RefreshToken.for_user(user)
            serializer.save()
            return Response(
                {'token': str(token.access_token), },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Обработчик для модели User."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = UsersPagination
    filter_backends = (filters.SearchFilter, )
    permission_classes = (AdminOnlyPermission, )
    search_fields = ('username', )
    lookup_field = 'username'


    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, username=kwargs['username'])
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        queryset = self.get_queryset()
        user = get_object_or_404(queryset, username=kwargs['username'])
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        get_object_or_404(queryset, username=kwargs['username']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)