"""Сериализаторы приложения API."""
import random

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db.models import Q

from core.send_mail import send_mail
from core.data_hash import hash_sha256
from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                message='Поле не соответсвует требованиям.',
                code='invalid_username',
            )
        ],
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, data):
        errors = {}
        username = data.get('username')
        email = data.get('email')

        if not email:
            errors['email'] = 'Введите правильный адрес электронной почты.'
        if not username:
            errors['username'] = 'Это поле не должно быть пустым.'
        if username == 'me':
            errors['username'] = 'Никнейм "me" запрещен.'

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        confirmation_code = random.randint(1000000, 9999999)

        user = User.objects.filter(
            Q(username=username) | Q(email=email)
        ).first()

        if user:
            if (
                user.email == email
                and user.username != username
                or (user.email != email and user.username == username)
            ):
                raise serializers.ValidationError(
                    {'error': 'Такой пользователь уже существует.'},
                )

            user.confirmation_code = hash_sha256(confirmation_code)
            print(user.confirmation_code)
            send_mail(
                from_email='yam.db.bot@support.com',
                to_email=email,
                subject='Confiramtion Code',
                message=f'Your confirmation code: {confirmation_code}',
            )
            user.save()
            return user
        user = User.objects.create(
            username=username,
            email=email,
            confirmation_code=hash_sha256(confirmation_code),
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

    def create(self, validated_data):
        user = get_object_or_404(User, username=validated_data.get('username'))
        user.is_active = True
        user.save()
        return user

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)
        print(confirmation_code)
        print(user.confirmation_code)
        if hash_sha256(confirmation_code) != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения.')
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для операций с моделью User."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                message='Поле не соответсвует требованиям.',
                code='invalid_username',
            )
        ],
    )

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

    def validate(self, data):
        errors = {}
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(
            Q(username=username) | Q(email=email)
        ).first()
        if not self.partial:
            if not email:
                errors['email'] = 'Введите правильный адрес электронной почты.'
            if not username:
                errors['username'] = 'Это поле не должно быть пустым.'
        if username == 'me':
            errors['username'] = 'Никнейм "me" запрещен.'
        if user:
            errors['user'] = (
                'Пользователь с таким username или email уже существует'
            )
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        """Метод для создания пользователя."""

        if validated_data.get('role') == ('admin' or 'moderator'):
            user = User.objects.create(
                **validated_data,
            )
            return user
        user = User.objects.create(
            **validated_data,
        )
        return user


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
            'rating'
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
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды')
        return data


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
