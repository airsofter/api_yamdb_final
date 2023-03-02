# from rest_framework import permissions, viewsets
# from rest_framework.generics import get_object_or_404
# from rest_framework.filters import SearchFilter
# from rest_framework.pagination import LimitOffsetPagination

# from .permissions import AuthorOrReadOnly
# from .serializers import CommentSerializer, GroupSerializer, PostSerializer
# from .serializers import FollowSerializer

# # from posts.models import Group, Post


# class GroupViewSet(viewsets.ReadOnlyModelViewSet):
#     """Вьюсет Group"""
#     # queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# class PostViewSet(viewsets.ModelViewSet):
#     """Вьюсет Post"""
#     # queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly,)
#     pagination_class = LimitOffsetPagination

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class CommentViewSet(viewsets.ModelViewSet):
#     """Вьюсет Comment"""
#     serializer_class = CommentSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         AuthorOrReadOnly,
#     )

#     def get_post(self):
#         post_id = self.kwargs['post_id']
#         return get_object_or_404(Post, pk=post_id)

#     def get_queryset(self):
#         return self.get_post().comments.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user, post=self.get_post())


# class FollowViewSet(viewsets.ModelViewSet):
#     """Вьюсет Follow"""
#     serializer_class = FollowSerializer
#     filter_backends = (SearchFilter,)
#     search_fields = ('following__username',)

#     def get_queryset(self):
#         return self.request.user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
