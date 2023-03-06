# import base64
import random

# from django.core.files.base import ContentFile
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

from core.send_mail import send_mail
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для показа произведений."""
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


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
