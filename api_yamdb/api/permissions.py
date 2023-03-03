"""Классы разрешений для приложения API."""
from rest_framework import permissions


class AuthorizedOrModeratorPermission(permissions.BasePermission):
    """Класс для контроля доступа к данным."""

    def has_object_permission(self, request, view, obj):
        return (
                    request.user.role == ('moderator' or 'admin')
                    or request.user == obj.user
        )


class AdministratorPermission(permissions.BasePermission):
    """Класс для контроля доступа к административным ресурсам."""

    def has_object_permission(self, request, view, obj):
        return request.user == 'admin'
