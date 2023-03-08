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

    def has_object_permission(self, request, view, obj):
        return (
                    request.user.role == 'admin'
        )