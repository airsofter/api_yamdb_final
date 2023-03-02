# import base64

# from django.core.files.base import ContentFile
# from rest_framework import serializers
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


# class GroupSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Group"""

#     class Meta:
#         pass


# class PostSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Post"""
#     author = SlugRelatedField(slug_field='username', read_only=True)
#     image = Base64ImageField(required=False, allow_null=True)

#     class Meta:
#         fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
#         # model = Post


# class CommentSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Comment"""
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username'
#     )

#     class Meta:
#         fields = ('id', 'author', 'text', 'created', 'post')
#         # model = Comment
#         read_only_fields = ('post',)


# class FollowSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Follow"""
#     # user = serializers.SlugRelatedField(
#     #     read_only=True,
#     #     slug_field='username',
#     #     default=serializers.CurrentUserDefault()
#     # )
#     # following = serializers.SlugRelatedField(
#     #     slug_field='username',
#     #     queryset=User.objects.all(),

#     # )

#     # class Meta:
#     #     model = Follow
#     #     fields = ('user', 'following')
#     #     validators = [
#     #         UniqueTogetherValidator(
#     #             queryset=Follow.objects.all(),
#     #             fields=['user', 'following']
#     #         )
#     #     ]

#     def validate(self, data):
#         if self.context['request'].user == data['following']:
#             raise serializers.ValidationError(
#                 'Нельзя подписаться на самого себя!')
#         return data
