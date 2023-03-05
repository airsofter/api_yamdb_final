"""Обработчики приложения API."""
import random

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework import permissions

from api.serializers import (
    SignupSerializer,
    TokenObtainSerializer,
    UsersSerializer,
)
from users.models import User
from api.permissions import AuthorizedOrModeratorPermission
from core.send_mail import send_mail


class SignupView(generics.CreateAPIView):
    """Обработчик для регистрации пользователей."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({
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
        print(user.password)
        print(serializer.validated_data['confirmation_code'])
        if (
            user.password
            == serializer.validated_data['confirmation_code']
        ):
            user.is_active = True
            print(user.is_active)
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
