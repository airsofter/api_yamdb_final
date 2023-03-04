# import base64
import random

# from django.core.files.base import ContentFile
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title

from core.send_mail import send_mail
from users.models import User


# class Base64ImageField(serializers.ImageField):
#     """Модуль с функциями декодирования base64 изображения"""
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='imgs.' + ext)

#         return super().to_internal_value(data)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""
    pass


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""
    pass


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для показа произведений."""
    pass


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""
    pass


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ревью."""
    pass


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "author", "review", "text", "pub_date")
        read_only_fields = ("review",)
        model = Comment


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
