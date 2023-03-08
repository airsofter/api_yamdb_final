"""Сериализаторы приложения API."""
import random
import hashlib

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db.models import Q

from core.send_mail import send_mail
from core.data_hash import hash_sha254
from users.models import User, ROLE_CHOICE
from reviews.models import Category, Comment, Genre, Review, Title


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
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
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if not email:
            raise serializers.ValidationError('Введите правильный адрес электронной почты.')
        if not username:
            raise serializers.ValidationError('Это поле не должно быть пустым.')
        if username == 'me':
            raise serializers.ValidationError('Никнейм "me" запрещен.')
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        confirmation_code = random.randint(1000000, 9999999)
        user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        print(user)

        if user:
            if user.email == email and user.username != username or (user.email != email and user.username == username):
                raise serializers.ValidationError('Такой пользователь уже существует.')

            user.confirmation_code = hash_sha254(confirmation_code)
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
            confirmation_code=confirmation_code,
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
        if confirmation_code != user.confirmation_code:

            raise serializers.ValidationError('Неверный код подтверждения.')
        return data

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

    def validate_email(self, value):
        """Метод для валидации email по количеству символов."""
        if len(value) > 254:
            raise serializers.ValidationError('Длина email не должна превышать 254 символа.')
        return value

    def create(self, validated_data):
        """Метод для создания пользователя."""

        if validated_data.get('role') == ('admin' or 'moderator'):
            user = User.objects.create_user(
                **validated_data,
                is_staff=True,
            )
            return user
        user = User.objects.create_user(
            **validated_data,
        )
        return user


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


    # def validate(self, data):
    #     """Метод для валидации email по количеству символов."""
    #     first_name = data.get('first_name')
    #     last_name = data.get('last_name')
    #     email = data.get('email')
    #     if not (email or first_name or last_name):
    #         raise serializers.ValidationError('Это поле не может быть пустым.')
    #     if len(email) > 254:
    #         raise serializers.ValidationError('Длина email не должна превышать 254 символа.')
    #     if len(last_name) > 150:
    #         raise serializers.ValidationError('Длина фамилии не должна превышать 150 символа.')
    #     if len(first_name) > 150:
    #         raise serializers.ValidationError('Длина имени не должна превышать 150 символа.')
    #     return data


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
