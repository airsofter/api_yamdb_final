"""Сериализаторы приложения API."""
import random

from rest_framework import serializers
from django.db import IntegrityError

from core.send_mail import send_mail
from users.models import User


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    def create(self, validated_data):

        user = User.objects.filter(
            username=validated_data.get('username'),
        ).first()
        username = validated_data.get('username')
        email = validated_data.get('email')
        confirmation_code = random.randint(1000000, 9999999)
        if user:
            send_mail(
                from_email='yam.db.bot@support.com',
                to_email=email,
                subject='Confiramtion Code',
                message=f'Your confirmation code: {confirmation_code}',
            )
            return user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=confirmation_code,
        )
        send_mail(
            from_email='yam.db.bot@support.com',
            to_email=email,
            subject='Confiramtion Code',
            message=f'Your confirmation code: {confirmation_code}',
        )
        return user

class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для операций с моделью User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def create(self, validated_data):
        """Метод дял создания пользователя."""

        if validated_data.get('role') == ('admin' or 'moderator'):
            user = User.objects.create_user(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                bio=validated_data.get('bio'),
                role=validated_data.get('role'),
                is_staff=True,
            )
            return user
        user = User.objects.create_user(
            **validated_data,
        )
        return user
