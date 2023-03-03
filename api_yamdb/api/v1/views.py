from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

from reviews.models import Genre, Category, Title, Review, Comment


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений"""
    serializer_class = TitleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly,
    )

    def get_post(self):
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


# class FollowViewSet(viewsets.ModelViewSet):
#     """Вьюсет Follow"""
#     serializer_class = FollowSerializer
#     filter_backends = (SearchFilter,)
#     search_fields = ('following__username',)

#     def get_queryset(self):
#         return self.request.user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
