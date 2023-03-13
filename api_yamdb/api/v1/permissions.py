"""Классы разрешений для приложения API."""
from rest_framework import permissions


class AuthorizedOrModeratorPermission(permissions.BasePermission):
    """Класс для контроля доступа к данным."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == ('moderator' or 'admin')
            or request.user == obj.user
        )


class AdminOnlyPermission(permissions.BasePermission):
    """Класс для контроля доступа к административным данным."""

    def has_permission(self, request, view):
        return ((
            request.user.is_authenticated
            and request.user.role == 'admin'
        )
            or request.user.is_staff
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """IsAuthorModeratorAdminOrReadOnly permission.
    1) Разрешает доступ к ресурсу, если используется безопасный метод или в
    случае, когда пользователь аутентифицирован.
    2) Разрешает доступ к объекту в случаях, когда используется безопасный
    метод или пользователь - это автор объекта, имеет роль
    модератора, администратора или суперпользователя.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ['moderator', 'admin']
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
