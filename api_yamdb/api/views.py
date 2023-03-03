"""Обработчики приложения API."""
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import SignupSerializer, TokenObtainSerializer
from users.models import User


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
