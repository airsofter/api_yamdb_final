# import base64
import random

# from django.core.files.base import ContentFile
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MaxValueValidator, MinValueValidator

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
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


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


