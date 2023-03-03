# import base64

# from django.core.files.base import ContentFile
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator


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


