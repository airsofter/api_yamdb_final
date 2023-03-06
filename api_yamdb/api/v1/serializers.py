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
