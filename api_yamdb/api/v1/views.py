"""Обработчики приложения API."""
import random

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, views
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework import permissions
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.serializers import (
    SignupSerializer,
    TokenObtainSerializer,
    UsersSerializer,
)
from users.models import User
from api.v1.permissions import AdminOnlyPermission
from core.data_hash import hash_sha254


class SignupView(generics.CreateAPIView):
    """Обработчик для регистрации пользователей."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                **serializer.data
            },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            user = get_object_or_404(User, username=serializer.validated_data.get('username'))
            token = RefreshToken.for_user(user)
            serializer.save()
            return Response(
                {'token': str(token.access_token),},
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

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me')
    def self_user(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = self.get_serializer(user, partial=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'self_user':
            return [permissions.IsAuthenticated(), ]
        return [AdminOnlyPermission(), ]
