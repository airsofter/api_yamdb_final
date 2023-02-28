from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """Изменение, удаление разрешено только автору."""
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.method in SAFE_METHODS)
