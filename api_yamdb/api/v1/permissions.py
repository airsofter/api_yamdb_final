"""Классы разрешений для приложения API."""
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


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
        return request.user.is_authenticated and request.user.role == 'admin' or request.user.is_staff
