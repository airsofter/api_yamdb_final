"""Сериализаторы приложения API."""
import random

from rest_framework import serializers

from core.send_mail import send_mail
from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        """Метод для создания пользователя."""

        confirmation_code = str(
            random.randint(1000000, 9999999)
        )
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=confirmation_code,
        )
        user.save()
        send_mail(
            subject='YamDB support!',
            message=f'Код подтверждения: {confirmation_code}',
            from_email='yam.db@support.com',
            to_email=validated_data['email']
        )
        return user


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
